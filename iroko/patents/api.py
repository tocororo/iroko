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

from iroko.api import IrokoBaseRecord
from iroko.organizations.api import OrganizationRecord
from iroko.persons.api import PersonRecord
from iroko.pidstore import pids
from iroko.utils import remove_nulls
from iroko.pidstore.pids import (
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
            pid_type=PATENT_PID_TYPE,
            object_type=IROKO_OBJECT_TYPE,
            getter=cls.get_record,
            )
        try:
            return resolver.resolve(str(pid_value))
        except Exception:
            pass

        for pid_type in identifiers_schemas:
            try:
                resolver.pid_type = pid_type
                schemapid, pat = resolver.resolve(pid_value)
                pid = PersistentIdentifier.get(PATENT_PID_TYPE, pat['id'])
                return pid, pat
            except Exception as e:
                pass
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
    def delete(cls, data, vendor=None, delindex=True, force=False):
        """Delete an IrokoRecord record."""
        assert data.get(cls.pid_uuid_field)
        pid = data.get(cls.pid_uuid_field)
        record = cls.get_record_by_pid_value(pid)
        pid.delete()
        result = record.delete(force=force)
        if delindex:
            try:
                RecordIndexer().delete(record)
            except NotFoundError:
                pass
        return result

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
