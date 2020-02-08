
import copy
from uuid import uuid4

from elasticsearch.exceptions import NotFoundError

from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.resolver import Resolver
from invenio_pidstore import current_pidstore

from invenio_records.api import Record

from iroko.pidstore.fetchers import iroko_uuid_fetcher
from iroko.pidstore.minters import iroko_uuid_minter
from iroko.pidstore.providers import IrokoUUIDProvider

from iroko.config import SEARCH_ELASTIC_HOSTS

from invenio_jsonschemas import current_jsonschemas

from flask import current_app

from elasticsearch_dsl.connections import connections

from elasticsearch_dsl import Search, Q

 
class IrokoAggs:

    @staticmethod
    def getAggrs(field, size=100):
        # Define a default Elasticsearch client
        client = connections.create_connection(hosts=SEARCH_ELASTIC_HOSTS)
        query_body = {
            "size": 0,
            "aggs": {
                "sources": {
                    "terms": {
                        "field": field,                        
                        "size" : size
                    }
                }
            }
        }
        s = Search(using=client, index="records").update_from_dict(query_body)
        t = s.execute()
        result = []
        for item in t.aggregations.sources.buckets:
            # item.key will the house number
            result.append({
                'key': item.key,
                'count': item.doc_count
            }) 
        # s = Search(using=client, index="records")
        
        # s.aggs.bucket('sources', 'terms', field='source.name', size=0)
        # s = s.execute()
        return result

class IrokoRecord (Record):
    """IrokoRecord class
    en general esto no esta muy bien, hay que profundizar en el problema de los PID, ahora mismo es solo un UUID, pero el PID no se puede generar a partir de la data... lo cual puede no ser muy bueno pues para manipular el record hay que saber el uuid, esto es contradictorio, pues en la data pueden venir doi, oai y otras formas de identificar el record..."""


    minter = iroko_uuid_minter
    fetcher = iroko_uuid_fetcher
    provider = IrokoUUIDProvider
    object_type = 'rec'
    uri_key = 'electronic_location_and_access'
    pid_field = 'id'

    _schema = "records/record-v1.0.0.json"

    @classmethod
    def create_or_update(cls, data, id_=None, dbcommit=False, reindex=False, record_uuid=None, **kwargs):
        """Create or update IrokoRecord."""
        # TODO: crar una funcion get_record_by_data, que reciba un data de un iroko record y busque, si existe, puede ser, por el source uuid y el original_identifier....
        if record_uuid:
            record = cls.get_record_by_pid(record_uuid, with_deleted=False)
            if record:
                # merged_data = cls._merge_uri(data, record)
                record.update(data, dbcommit=dbcommit, reindex=reindex)
                return record, 'updated'
        else:
            created_record = cls.create(data, id_=None, dbcommit=dbcommit, reindex=reindex)
            return created_record, 'created'

    @classmethod
    def create(cls, data, id_=None, dbcommit=False, reindex=False, **kwargs):
        """Create a new IrokoRecord."""
        data['$schema'] = current_jsonschemas.path_to_url(cls._schema)
        assert cls.minter
        assert not data.get(cls.pid_field)
        if not id_:
            id_ = uuid4()
        cls.minter(id_, data)
        data['suggest_title']= data.get('title')
        record = super(IrokoRecord, cls).create(data=data, id_=id_, **kwargs)
        if dbcommit:
            record.dbcommit(reindex)
        return record

    @classmethod
    def delete( cls, data, vendor=None, delindex=True, force=False):
        """Delete a IrokoRecord record."""
        assert data.get(cls.pid_field)
        pid = data.get(cls.pid_field)
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




