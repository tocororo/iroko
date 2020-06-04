from uuid import uuid4

from elasticsearch.exceptions import NotFoundError
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_jsonschemas import current_jsonschemas
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier
from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record

import iroko.pidstore.minters as iroko_minters
import iroko.pidstore.pids as pids
import iroko.pidstore.providers as iroko_providers
from iroko.pidstore.pids import identifiers_schemas


class OrganizationRecord(Record):
    _schema = "organizations/organization-v1.0.0.json"

    @classmethod
    def create_or_update(cls, org_uuid, data, dbcommit=False, reindex=False, **kwargs):
        """Create or update OrganizationRecord."""

        # assert org_uuid

        resolver = Resolver(
            pid_type=pids.ORGANIZATION_PID_TYPE,
            object_type=pids.ORGANIZATION_TYPE,
            getter=cls.get_record,
        )
        try:
            persistent_identifier, org = resolver.resolve(str(org_uuid))
            if org:
                print("{0}={1} found".format(pids.ORGANIZATION_PID_TYPE, org_uuid))
                org.update(data, dbcommit=dbcommit, reindex=reindex)
                return org, 'updated'
        except Exception:
            pass
        if pids.IDENTIFIERS_FIELD in data:
            for schema in identifiers_schemas:
                for identifier in data[pids.IDENTIFIERS_FIELD]:
                    if schema == identifier[pids.IDENTIFIERS_FIELD_TYPE]:
                        resolver.pid_type = schema
                        try:
                            persistent_identifier, org = resolver.resolve(str(identifier[pids.IDENTIFIERS_FIELD_VALUE]))
                            if org:
                                print("{0}={1} found".format(schema, str(identifier[pids.IDENTIFIERS_FIELD_VALUE])))
                                org.update(data, dbcommit=dbcommit, reindex=reindex)
                                return org, 'updated'
                        except Exception:
                            pass
        print("no pids found, creating organization")
        created_org = cls.create(data, id_=org_uuid, dbcommit=dbcommit, reindex=reindex)
        return created_org, 'created'

    @classmethod
    def create(cls, data, id_, dbcommit=False, reindex=False, **kwargs):
        """Create a new OrganizationRecord."""
        data['$schema'] = current_jsonschemas.path_to_url(cls._schema)
        if not id_:
            id_ = uuid4()

        iroko_minters.organization_uuid_minter(id_, data)
        iroko_minters.iroko_record_identifiers_minter(id_, data, pids.ORGANIZATION_TYPE)

        source = super(OrganizationRecord, cls).create(data=data, id_=id_, **kwargs)
        if dbcommit:
            db.session.commit()
            if reindex:
                RecordIndexer().index(source)
        return source

    @classmethod
    def delete(cls, data, delindex=True, force=False):
        """Delete a IrokoRecord record."""
        assert data.get(pids.ORGANIZATION_PID_FIELD)
        pid = data.get(pids.ORGANIZATION_PID_FIELD)
        org = cls.get_org_by_pid(pid, with_deleted=False)
        if org:
            result = org.delete(force=force)
            if delindex:
                try:
                    RecordIndexer().delete(org)
                except NotFoundError:
                    pass
            return result
        return False

    @classmethod
    def get_org_by_pid(cls, pid, with_deleted=False):
        resolver = Resolver(
            pid_type=pids.ORGANIZATION_PID_TYPE,
            object_type=pids.ORGANIZATION_TYPE,
            getter=cls.get_record,
        )
        try:
            persistent_identifier, org = resolver.resolve(str(pid))
            return org
        except PIDDoesNotExistError:
            return None


    def update(self, data, dbcommit=False, reindex=False):
        """Update data for record."""
        super(OrganizationRecord, self).update(data)
        super(OrganizationRecord, self).commit()
        print('update pids?')
        self.update_pids(data)
        if dbcommit:
            self.dbcommit(reindex)
        return self

    def update_pids(self, data):
        if pids.IDENTIFIERS_FIELD in data:
            for ids in data[pids.IDENTIFIERS_FIELD]:
                if ids['idtype'] in identifiers_schemas:
                    try:
                        pid = PersistentIdentifier.get(ids['idtype'], ids['value'])
                    except PIDDoesNotExistError:
                        print('!!!!!!!')
                        iroko_providers.IrokoRecordsIdentifiersProvider.create_pid(ids['idtype'],
                                                                                   object_type=pids.ORGANIZATION_TYPE,
                                                                                   object_uuid=self.id, data=data)

    def dbcommit(self, reindex=False, forceindex=False):
        """Commit changes to db."""
        db.session.commit()
        if reindex:
            self.reindex(forceindex=forceindex)

    def reindex(self, forceindex=False):
        """Reindex record."""
        if forceindex:
            RecordIndexer(version_type="external_gte").index(self)
        else:
            RecordIndexer().index(self)

