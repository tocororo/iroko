#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
import json
from iroko.api import IrokoBaseRecord
from iroko.organizations.api import OrganizationRecord
from iroko.persons.marshmallow.json import personMetadataSchema
from iroko.pidstore import pids
from iroko.utils import remove_nulls

from invenio_pidstore.resolver import Resolver

from iroko.pidstore.pids import PERSON_PID_TYPE

class PersonRecord (IrokoBaseRecord):
    _schema = "persons/person-v1.0.0.json"


    @classmethod
    def load_from_json_file(cls, file_path, org_pid):
        """bulk import of person from a json file asociated from specific organization
        expect spi format
        tries to create new persons profiles."""

        resolver = Resolver(
            pid_type=pids.PERSON_PID_TYPE,
            object_type=pids.IROKO_OBJECT_TYPE,
            getter=PersonRecord.get_record,
            )
        org = OrganizationRecord.get_record_by_pid_value(org_pid)
        if org:
            with open(file_path) as _file:
                persons = json.load(_file, object_hook=remove_nulls)
                for data in persons:
                    person = PersonRecord(data)
                    person  = fixture_spi_fields(person, org)
                    person.add_affiliation(org)
                    del person['_id']
                    print(person)
                    personRecord, msg = cls.resolve_and_update(data=person)
                    if not personRecord:
                        print("no pids found, creating organization")
                        personRecord = cls.create(person, iroko_pid_type=pids.PERSON_PID_TYPE)
                        msg = 'created'


    def add_affiliation(self, org: OrganizationRecord,
                        start_date=None, end_date=None,
                        role='member'):
        self.add_update_item_to_list_field(
            'affiliations', 'id',
            {
                'id': str(org.id),
                'identifiers': org.identifiers,
                'label':org['name'],
                'roles': [role]
                }
            )
    def add_email_address(self, email_address):
        if not 'email_addresses' in self:
            self['email_addresses'] = []
        is_new = True
        for address in self['email_addresses']:
            if address == email_address:
                is_new = False
        if is_new:
            self['email_addresses'].append(email_address)







def fixture_spi_fields(person: PersonRecord, org: OrganizationRecord):
    """hard code fixtures of spi data, coming from human resources of cuban institutions """
    country_code = 'cu'
    country = 'Cuba'
    if 'addresses' in org and len(org['addresses']) > 0:
        country_code = org['addresses'][0]['country_code']
        country = org['addresses'][0]['country']
        person['country'] = {'code': country_code, 'name': country}

    if 'institutional_email' in person:
        person.add_email_address(person['institutional_email'])
        del(person['institutional_email'])
    if 'lastName' in person:
        person['last_name'] = person['lastName']
        del(person['lastName'])

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
