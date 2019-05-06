
import copy
from uuid import uuid4

from elasticsearch.exceptions import NotFoundError

from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.resolver import Resolver
from invenio_pidstore import current_pidstore

from invenio_records.api import Record

from iroko.pidstore.fetchers import record_pid_fetcher
from iroko.pidstore.minters import build_record_pid, record_pid_minter
from iroko.pidstore.providers import IrokoRecordsPidProvider

from invenio_jsonschemas import current_jsonschemas

class IrokoRecord (Record):
    """IrokoRecord class"""


    minter = record_pid_minter
    fetcher = record_pid_fetcher
    provider = IrokoRecordsPidProvider
    object_type = 'rec'
    uri_key = 'electronic_location_and_access'

    _schema = "records/record-v1.0.0.json"

    @classmethod
    def create_or_update(
        cls,
        data,
        id_=None,
        dbcommit=False,
        reindex=False,
        vendor=None,
        **kwargs
    ):
        """Create or update sources record."""
        pid = build_record_pid(data, vendor)
        record = cls.get_record_by_pid(pid, with_deleted=False)
        if record:
            # merged_data = cls._merge_uri(data, record)
            record.update(data, dbcommit=dbcommit, reindex=reindex)
            return record, 'updated'
        else:
            created_record = cls.create(
                data,
                id_=None,
                vendor=vendor,
                dbcommit=dbcommit,
                reindex=reindex,
            )
            return created_record, 'created'

    @classmethod
    def create(
        cls,
        data,
        id_=None,
        dbcommit=False,
        reindex=False,
        vendor=None,
        **kwargs
    ):
        """Create a new sources record."""
        data['$schema'] = current_jsonschemas.path_to_url(cls._schema)
        assert cls.minter
        assert not data.get('pid')
        if not id_:
            id_ = uuid4()
        cls.minter(id_, data, vendor)
        record = super(IrokoRecord, cls).create(data=data, id_=id_, **kwargs)
        if dbcommit:
            record.dbcommit(reindex)
        return record

    @classmethod
    def delete(
        cls,
        data,
        vendor=None,
        delindex=True,
        force=False,
    ):
        """Delete a IrokoRecord record."""
        pid = build_record_pid(data, vendor)
        record = cls.get_record_by_pid(pid, with_deleted=False)
        pid.delete()
        result = record.delete(force=force)
        if delindex:
            try:
                RecordIndexer().delete(record)
            except NotFoundError:
                pass
        return result

    @classmethod
    def get_record_by_pid(cls, pid, with_deleted=False):
        """Get ebook record by pid value."""
        assert cls.provider
        resolver = Resolver(
            pid_type=cls.provider.pid_type,
            object_type=cls.object_type,
            getter=cls.get_record,
        )
        try:
            persistent_identifier, record = resolver.resolve(str(pid))
            return super(IrokoRecord, cls).get_record(
                persistent_identifier.object_uuid, with_deleted=with_deleted
            )
        except PIDDoesNotExistError:
            return None

    def update(self, data, dbcommit=False, reindex=False):
        """Update data for record."""
        super(IrokoRecord, self).update(data)
        super(IrokoRecord, self).commit()
        if dbcommit:
            self.dbcommit(reindex)
        return self

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
