#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
import json
from uuid import uuid4

from invenio_pidstore.resolver import Resolver

from iroko.api import IrokoBaseRecord
from iroko.organizations.api import OrganizationRecord
from iroko.pidstore import pids
from iroko.utils import remove_nulls

class ProjectRecord (IrokoBaseRecord):
    _schema = "projects/project-v2.0.0.json"

    @classmethod
    def load_from_json_file(cls, file_path, org_pid):
        """bulk import of person from a json file asociated from specific organization
        expect spi format
        tries to create new persons profiles."""

        resolver = Resolver(
            pid_type=pids.PROJECT_PID_TYPE,
            object_type=pids.IROKO_OBJECT_TYPE,
            getter=ProjectRecord.get_record,
        )
        org = OrganizationRecord.get_record_by_pid_value(org_pid)
        if org:
            with open(file_path) as _file:
                projects = json.load(_file, object_hook=remove_nulls)
                a = 0
                for data in projects:
                    a = a + 1
                    project = ProjectRecord(data)
                    project = fixture_spi_fields(project, org)
                    project.add_affiliation(org)
                    del project['_id']
                    print(project)
                    projectRecord = None
                    projectRecord, msg = cls.resolve_and_update(data=project)
                    print(projectRecord)
                    if not projectRecord:
                        print("no pids found, creating project")
                        projectRecord = cls.create(
                            project, iroko_pid_type=pids.PROJECT_PID_TYPE)
                        msg = 'created'
                print('====================================', a)

    @classmethod
    def create_project(cls, org_uuid, data, **kwargs):
        """Create or update Project."""
        ent = ProjectRecord(data)
        project = fixture_spi_fields(ent)
        cls.create(project,iroko_pid_type=pids.PROJECT_PID_TYPE)
        return project



    def add_affiliation(self, org: OrganizationRecord,
                        start_date=None, end_date=None,
                        role='member'):
        self.add_update_item_to_list_field(
            'affiliations', 'id',
            {
                'id': str(org.id),
                'identifiers': org.identifiers,
                'label': org['name'],
                'roles': [role]
            }
        )

    def add_email_address(self, email_address):
        new_eas = []
        if 'email_addresses' in self:
            new_eas = self['email_addresses']
        is_new = True
        for address in new_eas:
            if address == email_address:
                is_new = False
            else:
                if address != '':
                    new_eas.append(address)
        if is_new and email_address != '':
            new_eas.append(email_address)
        self['email_addresses'] = new_eas


def fixture_spi_fields(project: ProjectRecord, ):
    new_identifiers = []
    for identifier in project[pids.IDENTIFIERS_FIELD]:
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
    project[pids.IDENTIFIERS_FIELD] = new_identifiers
    return project
