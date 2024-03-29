#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
import traceback

from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from flask import current_app
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.errors import PIDDeletedError, PIDDoesNotExistError
from invenio_pidstore.models import PIDStatus, PersistentIdentifier
from invenio_pidstore.resolver import Resolver

import iroko.pidstore.minters as iroko_minters
from iroko.api import IrokoBaseRecord
from iroko.pidstore import pids
from iroko.pidstore import providers


# from invenio_records.api import Record



class IrokoRecord(IrokoBaseRecord):
    """IrokoRecord class
    en general esto no esta muy bien, hay que profundizar en el problema de los PID, ahora mismo
    es solo un UUID, pero el PID no se puede generar a partir de la data... lo cual puede no ser
    muy bueno pues para manipular el record hay que saber el uuid, esto es contradictorio,
    pues en la data pueden venir doi, oai y otras formas de identificar el record..."""

    _schema = "records/record-v1.0.0.json"

    @classmethod
    def create_or_update(
        cls, data, id_=None, dbcommit=False, reindex=False, record_uuid=None, **kwargs
        ):
        """Create or update IrokoRecord."""

        record, info = cls.resolve_and_update(iroko_uuid=id_, data=data)
        if not record:
            created_record = cls.create(data, id_=None, dbcommit=dbcommit, reindex=reindex)
            return created_record, 'created'
        return record, info

        # if record_uuid:
        #     record = cls.get_record_by_pid_value(record_uuid)
        #     if record:
        #         # merged_data = cls._merge_uri(data, record)
        #         record.update(data, dbcommit=dbcommit, reindex=reindex)
        #         return record, 'updated'
        # else:
        #     record = cls.get_record_by_data(data)
        #     if record:
        #         record.update_record(data, dbcommit=dbcommit, reindex=reindex)
        #         return record, 'updated'
        #     created_record = cls.create(data, id_=None, dbcommit=dbcommit, reindex=reindex)
        #     return created_record, 'created'

    @classmethod
    def create(cls, data, id_=None, object_uuid=None, **kwargs):
        """Create a new IrokoRecord."""

        data['suggest_title'] = data.get('title')
        record = super(IrokoRecord, cls).create(data=data,
                                                iroko_pid_type=pids.RECORD_PID_TYPE,
                                                iroko_pid_value=id_,
                                                object_uuid=object_uuid,
                                                **kwargs)
        iroko_minters.iroko_source_oai_minter(record.id, data)

        return record

    @classmethod
    def delete(cls, data, vendor=None, delindex=True, force=False):
        """Delete a IrokoRecord record."""
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


    @classmethod
    def get_record_by_data(cls, data):
        # depending of the providers this method can be more complex, meaning using other
        # external PIDs like url or doi

        # assert cls.oai_provider
        resolver = Resolver(
            pid_type= providers.IrokoSourceOAIProvider.pid_type,
            object_type=pids.IROKO_OBJECT_TYPE,
            getter=cls.get_record,
            )
        try:
            pid = providers.IrokoSourceOAIProvider.get_pid_from_data(data=data)
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

