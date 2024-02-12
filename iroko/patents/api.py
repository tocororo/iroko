#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
import json

from elasticsearch.exceptions import NotFoundError
from invenio_pidstore.resolver import Resolver
from invenio_pidstore.models import PersistentIdentifier
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.errors import PIDDeletedError, PIDDoesNotExistError
from sqlalchemy.exc import NoResultFound



from iroko.api import IrokoBaseRecord
from iroko.organizations.api import OrganizationRecord
from iroko.persons.api import PersonRecord
from iroko.pidstore import pids
from iroko.utils import remove_nulls
from iroko.pidstore.pids import (
    IDENTIFIERS_FIELD,  IDENTIFIERS_FIELD_VALUE,
    IDENTIFIERS_FIELD_TYPE, IROKO_OBJECT_TYPE, PATENT_PID_TYPE, identifiers_schemas,
    )


class PatentRecord (IrokoBaseRecord):
    _schema = "patents/patent-v1.0.0.json"

    @classmethod
    def load_from_json_file(cls, file_path):
        """bulk import of patent from a json file
        expect spi format"""

        resolver = Resolver(
            pid_type=pids.PATENT_PID_TYPE,
            object_type=pids.IROKO_OBJECT_TYPE,
            getter=PatentRecord.get_record,
            )
        # per = PersonRecord.get_record_by_pid_value(per_pid)
        with open(file_path) as _file:
            patents = json.load(_file, object_hook=remove_nulls)
            a = 0
            for data in patents:
                a = a + 1
                patent = PatentRecord(data)
                del patent['_id']
                print(patent)
                patentRecord = None
                patentRecord, msg = cls.resolve_and_update(data=patent)
                print(patentRecord)
                if not patentRecord:
                    print("no pids found, creating patent")
                    patentRecord = cls.create(patent, iroko_pid_type=pids.PATENT_PID_TYPE)
                    msg = 'created'
            print('====================================', a)

    @classmethod
    def get_pat_by_pid(cls, pid_value, with_deleted=False):
        resolver = Resolver(
            pid_type='doi',
            object_type=IROKO_OBJECT_TYPE,
            getter=cls.get_record,
            )
        try:
            return resolver.resolve(str(pid_value))
        except Exception:
            pass

        # for pid_type in identifiers_schemas:
        #     try:
        #         resolver.pid_type = pid_type
        #         schemapid, pat = resolver.resolve(pid_value)
        #         pid = PersistentIdentifier.get(PATENT_PID_TYPE, pat['id'])
        #         return pid, pat
        #     except Exception as e:
        #         pass
        return None, None

    @classmethod
    def create_or_update(cls, pat_uuid, data, **kwargs):
        """Create or update PatentRecord."""

        # assert pat_uuid
        pat, msg = cls.resolve_and_update(pat_uuid, data)
        # if resolve_and_update do no return, then is not existed pat, so trying to create one
        if not pat:
            print("no pids found, creating patent")
            created_pat = cls.create(data, iroko_pid_type=pids.PATENT_PID_TYPE,
                                    iroko_pid_value=pat_uuid)
            pat = created_pat
            msg = 'created'

        return pat, msg


    @classmethod
    def update_imported(cls, pat_uuid=None, data={}):
        resolver = Resolver(
            pid_type=pids.RECORD_PID_TYPE,
            object_type=IROKO_OBJECT_TYPE,
            getter=cls.get_record,
        )
        if IDENTIFIERS_FIELD in data:  # Si no lo encontro por el uuid, igual se intenta buscar
            # desde cualquier otri pid
            for schema in identifiers_schemas:
                for identifier in data[IDENTIFIERS_FIELD]:
                    if schema == identifier[IDENTIFIERS_FIELD_TYPE]:
                        # print("identifier ------    ", identifier)
                        resolver.pid_type = schema
                        try:
                            persistent_identifier, rec = resolver.resolve(
                                str(identifier[IDENTIFIERS_FIELD_VALUE])
                                )
                            print('<<<<<<<<<<<<<<<<<<')
                            print('rec= ', json.dumps(rec, indent=3))
                            print('data= ', json.dumps(rec, indent=3))
                            if rec:
                                resolver.pid_type = pids.PATENT_PID_TYPE
                                uuid = rec["id"]
                                print(uuid)
                                try:
                                    persistent_identifier, rec = resolver.resolve(str(uuid))
                                    print('rec= ', json.dumps(rec, indent=3))
                                    if rec:
                                        print('REC',rec)
                                        rec.update(data)
                                        return rec, 'updated'
                                except Exception:
                                    pass
                                print('========================================')

                                print('>>>>>>>>>>>>>>>>>>>>')
                                print('rec updated: ', rec)
                                return rec, 'updated'
                        except PIDDoesNotExistError as pidno:
                            print(
                                "PIDDoesNotExistError:  {0} == {1}".format(
                                    schema,
                                    str(
                                        identifier[
                                            IDENTIFIERS_FIELD_VALUE]
                                        )
                                    )
                                )
                        except (PIDDeletedError, NoResultFound) as ex:
                            cls.__delete_pids_without_object(data[IDENTIFIERS_FIELD])
                        except Exception as e:
                            print('-------------------------------')
                            # print(str(e))
                            print(traceback.format_exc())
                            print('-------------------------------')
                            pass
        return None, None

    @classmethod
    def delete(cls, pid, vendor=None, delindex=True, force=False):
        """Delete an IrokoRecord record."""
        record = cls.get_record_by_pid_value(pid)
        pid.replace(pid, '')
        result = record.delete(force=force)
        if delindex:
            try:
                RecordIndexer().delete(record)
            except NotFoundError:
                pass
        return result


    def fix_patents_imported(patent):
        if 'identifiers' in patent:
            patent['identifiers'] = patent['identifiers']

        if 'country' in patent:
            patent['country'] = patent['country']
        else:
            patent['country'] = {'code': '', 'name': ''}

        if 'affiliations' in patent:
            patent['affiliations'] = patent['affiliations']
        else:
            patent['affiliations'] = []

        if 'authors' in patent:
            patent['authors'] = patent['authors']
        else:
            patent['authors'] = []

        if 'language' in patent:
            patent['language'] = patent['language']
        else:
            patent['language'] = ''

        if 'classification' in patent:
            patent['classification'] = patent['classification']
        else:
            patent['classification'] = ''

        if 'link' in patent:
            patent['link'] = patent['link']
        else:
            patent['link'] = ''

        if 'summary' in patent:
            patent['summary'] = patent['summary']
        else:
            patent['summary'] = ''

        return patent

    def fix_gp_imported(patent):
        if 'id' in patent:
            identifiers = []
            identifiers.append({
                'idtype': 'doi',
                'value': patent['id']
            })
            patent['identifiers'] = identifiers
            del patent['id']

        if 'assignee' in patent:
            affiliations = []
            for affiliation in patent['assignee']:
                affiliations.append({
                    'identifiers': [],
                    'name': affiliation
                })
            patent['affiliations'] = affiliations
            del patent['assignee']

        else :
            patent['affiliations'] = []

        if 'author' in patent and len(patent['author']) > 0:
            authors = []
            for author in patent['author']:
                authors.append({
                    'identifiers': [],
                    'name': author
                })
            patent['authors'] = authors
            del patent['author']

        else :
            patent['authors'] = []

        patent['language'] = ''
        patent['country'] = {'code': '', 'name': ''}
        patent['classification'] = ''
        del patent['']

        if 'filing/creation date' in patent:
            patent['creation_date'] = patent['filing/creation date']
            del patent['filing/creation date']

        if 'grant date' in patent:
            patent['grant_date'] = patent['grant date']
            del patent['grant date']

        if 'priority date' in patent:
            del patent['priority date']

        if 'publication date' in patent:
            patent['publication_date'] = patent['publication date']
            del patent['publication date']

        if 'result link' in patent:
            patent['link'] = patent['result link']
            del patent['result link']

        return patent




def fixture_spi_fields(person: PersonRecord, org: OrganizationRecord):
    """hard code fixtures of spi data, coming from human resources of cuban institutions """
    country_code = 'cu'
    country = 'Cuba'
    if 'addresses' in org and len(org['addresses']) > 0:
        country_code = org['addresses'][0]['country_code']
        country = org['addresses'][0]['country']
    person['country'] = {'code': country_code, 'name': country}

    if 'institutional_email' in person and len(person['institutional_email']) > 0:
        person.add_email_address(person['institutional_email'])
    if 'emails' in person:
        for ma in person['emails']:
            person.add_email_address(person['institutional_email'])
    if 'lastName' in person:
        person['last_name'] = person['lastName']

    person.pop('lastName')
    person.pop('institutional_email')
    person.pop('emails')

    new_identifiers = []
    for identifier in person[pids.IDENTIFIERS_FIELD]:
        if identifier['idtype'] == 'noCi':
            new_identifiers.append({
                'idtype': 'dni',
                'value': 'dni:' + country_code + '.' + identifier['idvalue'],
                })
        elif identifier['idtype'] == 'idExpediente':
            new_identifiers.append({
                'idtype': 'hrid',
                'value': 'hrid:' + str(org.id) + '.' + identifier['idvalue'],
                })
        else:
            new_identifiers.append(identifier)
    person[pids.IDENTIFIERS_FIELD] = new_identifiers
    return person
