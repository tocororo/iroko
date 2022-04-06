#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
import traceback
from uuid import uuid4

from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from flask import current_app
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_jsonschemas import current_jsonschemas
from invenio_pidstore.errors import PIDDeletedError, PIDDoesNotExistError
from invenio_pidstore.models import PIDStatus, PersistentIdentifier
from invenio_pidstore.resolver import Resolver
# from invenio_records.api import Record
from invenio_records_files.api import Record

import iroko.pidstore.fetchers as iroko_fetchers
import iroko.pidstore.minters as iroko_minters
import iroko.pidstore.providers as iroko_providers
from iroko.pidstore import pids


class IrokoAggs:

    @staticmethod
    def getAggrs(field, size=100):
        # Define a default Elasticsearch client
        client = connections.create_connection(hosts=current_app.config["SEARCH_ELASTIC_HOSTS"])
        query_body = {
            "size": 0,
            "aggs": {
                "sources": {
                    "terms": {
                        "field": field,
                        "size": size
                        }
                    }
                }
            }
        s = Search(using=client, index="records").update_from_dict(query_body)
        t = s.execute()
        # # print(t.aggregations.sources.buckets)
        # return t.aggregations.sources.buckets
        result = []
        for item in t.aggregations.sources.buckets:
            # item.key will the house number
            result.append(
                {
                    'key': item.key,
                    'doc_count': item.doc_count
                    }
                )
        # s = Search(using=client, index="records")

        # s.aggs.bucket('sources', 'terms', field='source.name', size=0)
        # s = s.execute()
        return result


class IrokoRecord(Record):
    """IrokoRecord class
    en general esto no esta muy bien, hay que profundizar en el problema de los PID, ahora mismo
    es solo un UUID, pero el PID no se puede generar a partir de la data... lo cual puede no ser
    muy bueno pues para manipular el record hay que saber el uuid, esto es contradictorio,
    pues en la data pueden venir doi, oai y otras formas de identificar el record..."""

    uuid_minter = iroko_minters.iroko_uuid_minter
    uuid_fetcher = iroko_fetchers.iroko_uuid_fetcher
    uuid_provider = iroko_providers.IrokoUUIDProvider

    oai_minter = iroko_minters.iroko_source_oai_minter
    oai_fetcher = iroko_fetchers.iroko_source_oai_fetcher
    oai_provider = iroko_providers.IrokoSourceOAIProvider

    object_type = 'rec'
    uri_key = 'electronic_location_and_access'
    pid_uuid_field = 'id'

    _schema = "records/record-v1.0.0.json"

    @classmethod
    def create_or_update(
        cls, data, id_=None, dbcommit=False, reindex=False, record_uuid=None, **kwargs
        ):
        """Create or update IrokoRecord."""

        if record_uuid:
            record = cls.get_record_by_pid(record_uuid, with_deleted=False)
            if record:
                # merged_data = cls._merge_uri(data, record)
                record.update(data, dbcommit=dbcommit, reindex=reindex)
                return record, 'updated'
        else:
            record = cls.get_record_by_data(data)
            if record:
                record.update(data, dbcommit=dbcommit, reindex=reindex)
                return record, 'updated'
            created_record = cls.create(data, id_=None, dbcommit=dbcommit, reindex=reindex)
            return created_record, 'created'

    @classmethod
    def create(cls, data, id_=None, dbcommit=False, reindex=False, **kwargs):
        """Create a new IrokoRecord."""
        data['$schema'] = current_jsonschemas.path_to_url(cls._schema)
        assert cls.uuid_minter
        assert cls.oai_minter
        assert not data.get(cls.pid_uuid_field)
        if not id_:
            id_ = uuid4()
        cls.uuid_minter(id_, data)
        # # print("######### {0}".format(id_))
        cls.oai_minter(id_, data)
        data['suggest_title'] = data.get('title')
        record = super(IrokoRecord, cls).create(data=data, id_=id_, **kwargs)
        if dbcommit:
            record.dbcommit(reindex)
        return record

    @classmethod
    def delete(cls, data, vendor=None, delindex=True, force=False):
        """Delete a IrokoRecord record."""
        assert data.get(cls.pid_uuid_field)
        pid = data.get(cls.pid_uuid_field)
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
        assert cls.uuid_provider
        resolver = Resolver(
            pid_type=cls.uuid_provider.pid_type,
            object_type=cls.object_type,
            getter=cls.get_record,
            )
        try:
            persistent_identifier, record = resolver.resolve(str(pid))
            return record
            # return super(IrokoRecord, cls).get_record(
            #     persistent_identifier.object_uuid, with_deleted=with_deleted
            # )
        except PIDDoesNotExistError:
            return None

    @classmethod
    def get_record_by_data(cls, data):
        # depending of the providers this method can be more complex, meaning using other
        # external PIDs like url or doi
        assert cls.oai_provider
        resolver = Resolver(
            pid_type=cls.oai_provider.pid_type,
            object_type=cls.object_type,
            getter=cls.get_record,
            )
        try:
            pid = cls.oai_provider.get_pid_from_data(data=data)
            try:
                persistent_identifier, record = resolver.resolve(str(pid))
                return record
            except PIDDeletedError:
                PersistentIdentifier.query.filter_by(
                    pid_type=pids.RECORD_SOURCE_OAI_PID_TYPE,
                    pid_value=str(pid)
                    ).delete()
                db.session.commit()
                return None
            except Exception as e:
                print(traceback.format_exc())
                persistent_identifier = PersistentIdentifier.get(
                    pids.RECORD_SOURCE_OAI_PID_TYPE, str(pid)
                    )
                persistent_identifier.unassign()
                persistent_identifier.status == PIDStatus.NEW
                persistent_identifier.delete()
                db.session.commit()
                return None
            # return super(IrokoRecord, cls).get_record(
            #     persistent_identifier.object_uuid, with_deleted=with_deleted
            # )

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
