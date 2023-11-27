import traceback
from datetime import date
from uuid import uuid4

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from flask import current_app
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_jsonschemas import current_jsonschemas
from invenio_pidstore.errors import (
    PIDDeletedError, PIDDoesNotExistError, PIDMissingObjectError,
    PIDRedirectedError,
    )
from invenio_pidstore.models import PIDStatus, PersistentIdentifier
from invenio_pidstore.resolver import Resolver
from invenio_records_files.api import Record
from sqlalchemy.exc import NoResultFound

import iroko.pidstore.providers as iroko_providers
from iroko.pidstore import pids
from iroko.pidstore.minters import identifiers_minter, iroko_uuid_minter
from iroko.pidstore.pids import (
    IDENTIFIERS_FIELD, IDENTIFIERS_FIELD_TYPE, IDENTIFIERS_FIELD_VALUE, IROKO_OBJECT_TYPE,
    IROKO_UUID_PID_TYPES, identifiers_schemas,
    )
import logging

logger = logging.getLogger("iroko")

# TODO: use idtype = fields.Str(validate=validate.OneOf(choices=IdentifierTypeEnum))
# en cada identifiers comprobar esto..



class IrokoBaseRecord(Record):
    """Class with common functions to Iroko Records"""

    # Note: self['field'] == self.model.json['field'] is True
    @classmethod
    def create(cls, data=None, iroko_pid_type=None, iroko_pid_value=None, object_uuid=None,
               **kwargs):
        """Create a new IrokoRecord."""
        assert data
        data['$schema'] = current_jsonschemas.path_to_url(cls._schema)

        if not iroko_pid_value:
            iroko_pid_value = uuid4()

        if not object_uuid:
            object_uuid = uuid4()

        try:

            pid = iroko_uuid_minter(pid_type=iroko_pid_type, pid_value=iroko_pid_value,
                                    object_type=pids.IROKO_OBJECT_TYPE,
                                    object_uuid=object_uuid, data=data)

            identifiers_minter(object_uuid, data, IROKO_OBJECT_TYPE)

            rec = super(IrokoBaseRecord, cls).create(data=data, id_=str(object_uuid),
                                                     with_bucket=False, **kwargs)
            db.session.commit()
            RecordIndexer().index(rec)

            return rec

        except Exception as ex:
            # TODO: try to rollback pids and record creation, if any...
            logger.exception(traceback.format_exc())

            raise  ex

        return None



    @classmethod
    def resolve_and_update(cls, iroko_uuid=None, data={}, **kwargs):
        """
        return tuple [updated object, info string]
        """
        logger.info("resolve and update =============================={0}".format(data))

        resolver = Resolver(
            pid_type=pids.RECORD_PID_TYPE,
            object_type=IROKO_OBJECT_TYPE,
            getter=cls.get_record,
            )

        if iroko_uuid:
            for pid_type in pids.IROKO_UUID_PID_TYPES:
                resolver.pid_type = pid_type
                try:
                    persistent_identifier, rec = resolver.resolve(str(iroko_uuid))
                    if rec:
                        logger.info("{0}={1} found".format(pid_type, iroko_uuid))
                        return rec.try_update(data)
                except  Exception:
                    pass

        if "id" in data:
            iroko_uuid = data['id']
            for pid_type in pids.IROKO_UUID_PID_TYPES:
                resolver.pid_type = pid_type
                try:
                    persistent_identifier, rec = resolver.resolve(str(iroko_uuid))
                    if rec:
                        logger.info("{0}={1} found in data[id]".format(pid_type, iroko_uuid))
                        return rec.try_update(data)
                except Exception:
                    pass
        if IDENTIFIERS_FIELD in data:  # Si no lo encontro por el uuid, igual se intenta buscar
            # desde cualquier otro pid
            for schema in identifiers_schemas:
                for identifier in data[IDENTIFIERS_FIELD]:
                    if schema == identifier[IDENTIFIERS_FIELD_TYPE]:
                        # print("identifier ------    ", identifier)
                        resolver.pid_type = schema
                        try:
                            persistent_identifier, rec = resolver.resolve(
                                str(identifier[IDENTIFIERS_FIELD_VALUE])
                                )
                            if rec:
                                logger.info(
                                    "{0}={1} found in data[identifiers]".format(
                                        schema, str(
                                            identifier[IDENTIFIERS_FIELD_VALUE]
                                            )
                                        )
                                    )
                                return rec.try_update(data)


                        except PIDDoesNotExistError as pidno:
                            logger.exception(
                                "------------------------------------------------------  "
                                "PIDDoesNotExistError:  {0} == {1}".format(
                                    schema,
                                    str(
                                        identifier[
                                            IDENTIFIERS_FIELD_VALUE]
                                        )
                                    )
                                )
                            pass
                        except (PIDDeletedError) as ex:
                            logger.exception(
                                "------------------------------------------------------ "
                                "PIDDeletedError:  {0} == {1}".format(
                                    schema,
                                    str(
                                        identifier[
                                            IDENTIFIERS_FIELD_VALUE]
                                        )
                                    )
                                )
                            pass
                        except (PIDRedirectedError) as ex:
                            logger.exception(
                                "------------------------------------------------------  "
                                "PIDRedirectedError:  {0} == {1}".format(
                                    schema,
                                    str(
                                        identifier[
                                            IDENTIFIERS_FIELD_VALUE]
                                        )
                                    )
                                )
                            pass
                        except (PIDMissingObjectError) as ex:
                            logger.exception(
                                "------------------------------------------------------  "
                                "PIDMissingObjectError:  {0} == {1}".format(
                                    schema,
                                    str(
                                        identifier[
                                            IDENTIFIERS_FIELD_VALUE]
                                        )
                                    )
                                )
                            pass
                        except (NoResultFound) as ex:
                            logger.exception(
                            "------------------------------------------------------  "
                            "NoResultFound:  {0} == {1}".format(
                                schema,
                                str(
                                    identifier[
                                        IDENTIFIERS_FIELD_VALUE]
                                    )
                                )
                            )
                            pass
                            # TODO:
                            # esto esta mal: __delete_pids_without_object
                            # No tiene sentido eliminar todos los pids si
                            # uno esta eliminado, se puso para arreglar datos inestables.
                            # hoy (17/nov/2023), lo quito porque si un pid esta marcado como
                            # eliminado, no se debe eliminar de la base de datos, puesto que ese
                            # pid ya esta reservado.
                            # Esto es importante para cuando este en produccion el sistema.
                            # cls.__delete_pids_without_object(data[IDENTIFIERS_FIELD])
                        except Exception as e:
                            logger.exception(
                                "------------------------------------------------------     {"
                                "0}".format(traceback.format_exc()))
                            pass
        return None, None
    def try_update(self, data):
        try:
            self.update(data)
            logger.debug("UPDATED: {0}".format(self))
            return self, 'updated'
        except Exception as e:
            error = traceback.format_exc()
            logger.exception(
                "------------------------------------------------------     {"
                "0}".format(error))
            return None, str(error)

    @classmethod
    def get_record_by_pid(cls, record_pid_type, pid_value, with_deleted=False):
        resolver = Resolver(
            pid_type=record_pid_type,
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
                schemapid, rec = resolver.resolve(pid_value)
                pid = PersistentIdentifier.get(record_pid_type, rec['id'])
                return pid, rec
            except Exception as e:
                pass
        return None, None

    @classmethod
    def get_record_by_pid_value(cls, pid_value):
        """return the record based on any pid, in the id field or in identifiers field"""
        resolver = Resolver(object_type=IROKO_OBJECT_TYPE, getter=cls.get_record)
        for pid_type in IROKO_UUID_PID_TYPES:
            try:
                resolver.pid_type = pid_type
                pid, rec = resolver.resolve(pid_value)
                return rec
            except Exception as e:
                pass
        for pid_type in identifiers_schemas:
            try:
                resolver.pid_type = pid_type
                pid, rec = resolver.resolve(pid_value)
                return rec
            except Exception as e:
                pass
        return None

    def get_iroko_uuid(self):
        """All iroko records has a field in the metadata called 'id' """
        return self.model.json['id']

    iroko_uuid = property(get_iroko_uuid)

    def get_identifiers(self):
        return self.model.json['identifiers']

    identifiers = property(get_identifiers)

    def get_field(self, field_name):
        """helper function to get any field of the metadata model
        if the field dont exists return empty string """
        if field_name in self.model.json:
            return self.model.json[field_name]
        return ''

    def update(self, data=None, dbcommit=True, reindex=True, override_pids=True):
        """ Update data for record.
        override_pids, if True
        """
        logger.info('begin update')

        self['_save_info_updated'] = str(date.today())

        if data and type(data) == dict:
            super(IrokoBaseRecord, self).update(data)
        else:
            data = dict(self)
            super(IrokoBaseRecord, self).update(data)

        logger.info('update pids ')
        # TODO: improve/clarify update pids
        self._update_pids(override_pids)

        super(IrokoBaseRecord, self).commit()
        if dbcommit:
            self.dbcommit(reindex)
        logger.info('UPDATED', self.model.json)
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

    def add_identifier(self, idtype, value):
        self.add_update_item_to_list_field(
            pids.IDENTIFIERS_FIELD, 'idtype',
            {
                'idtype': idtype,
                'value': value
                }
            )

    def add_update_item_to_list_field(self, list_key, list_item_id_key, item_to_add):
        """helper function to add or update an item to a list field of the record (dict).
        list_key: the name of the field list in the record
        list_item_id_key: the name of the identifier field in the list field
        item_to_add: item to add or update to the list.

        example: rec.add_update_item_to_list_field
        """
        if list_key not in self:
            self[list_key] = []
        if type(self[list_key]) == list:
            for item in self[list_key]:
                if type(item) == dict() and item[list_item_id_key] == item_to_add[list_item_id_key]:
                    item.update(item_to_add)
                    return
                elif item == item_to_add:
                    return
            self[list_key].append(item_to_add)

    def _update_pids(self, override_pids=True):

        if pids.IDENTIFIERS_FIELD in self:
            for ids in self[pids.IDENTIFIERS_FIELD]:
                if ids['idtype'] in identifiers_schemas: # solo acepta tipos de identificadores declarados.
                    if ids['value'] != '': # debe tener un valor distinto de vacio
                        try:
                            pid = PersistentIdentifier.get(ids['idtype'], ids['value'])
                            obj_uuid = pid.get_assigned_object(pids.IROKO_OBJECT_TYPE)
                            logger.info('!!!!!!!')
                            logger.info('{0}-{1}'.format(ids['idtype'], ids['value']))
                            logger.info('!!!!!!!')
                            if obj_uuid != self.id:
                                logger.info('!!!!!!!******')
                                logger.info(
                                    'PIDObjectAlreadyAssigned{0}-{1}'.format(
                                        ids['idtype'], ids['value']
                                        )
                                    )
                                # override_pids
                                if override_pids:
                                    logger.info("assign pid to self")
                                    pid.assign(pids.IROKO_OBJECT_TYPE, self.id, override_pids)

                        # except PIDObjectAlreadyAssigned as e:
                        #     print('!!!!!!! what?')
                        #     raise e
                        except PIDDoesNotExistError:

                            iroko_providers.IrokoRecordsIdentifiersProvider.create_pid(
                                ids['idtype'], ids['value'],
                                object_type=pids.IROKO_OBJECT_TYPE,
                                object_uuid=self.id, data=self
                                )
                    else:
                        self[pids.IDENTIFIERS_FIELD].remove(ids)
                else:
                    self[pids.IDENTIFIERS_FIELD].remove(ids)

        # esto lo que hace es que adiciona al campo identifiers, el campo id, como un
        # identificador de sceiba, el tipo de pid, en este caso es irouid, srcid, perid, orgid,
        # etc... en dependencia del tipo de record.
        # La idea es siempre tener los records con al menos un identifier, al menos el
        # identificador de iroko.
        # Tener en cuenta que esto es automatico, es decir , con independencia de los
        # identificadores que pase el usuario IrokoRecord siempre va a poner un identificador que
        # es igual al id del record.
        self._update_irokoUUID_in_identifiers()

        # TODO: que pasa si se eliminan PIDS:
        # hay que hacer un metodo aqui que busque todos los pids del objeto actual, si existe
        # algun pid que referencia al objeto actual, pero que no esta dentro de identifiers,
        # entonces ese pid debe marcarse como Deleted.


    def _update_irokoUUID_in_identifiers(self):
        """
        este metodo adiciona al campo identifiers, el campo id, como un
        identificador de sceiba, el tipo de pid, en este caso es irouid, srcid, perid, orgid,
        etc... en dependencia del tipo de record
        """
        resolver = Resolver(
            pid_type=pids.RECORD_PID_TYPE,
            object_type=IROKO_OBJECT_TYPE,
            getter=self.get_record,
            )

        iroko_uuid = self.iroko_uuid
        for pid_type in pids.IROKO_UUID_PID_TYPES:
            resolver.pid_type = pid_type
            try:
                persistent_identifier, rec = resolver.resolve(iroko_uuid)
                if persistent_identifier and rec:
                    self.add_identifier(pid_type, iroko_uuid)
            except  Exception:
                pass

    @classmethod
    def __delete_pids_without_object(cls, pid_list):
        try:
            # print('pids list: ')
            # print(pid_list)
            if pid_list and len(pid_list) > 0:
                for identifier in pid_list:
                    pid_type = identifier[IDENTIFIERS_FIELD_TYPE]
                    pid_value = identifier[IDENTIFIERS_FIELD_VALUE]
                    # print('pid type deleting: ')
                    # print(pid_type)
                    # print(pid_value)
                    pid_item = PersistentIdentifier.get(pid_type, pid_value)
                    pid_item.status = PIDStatus.NEW
                    # print('getting pid item: ')

                    if pid_item.delete():
                        db.session.commit()
                        # print("***************** DELETED!!!!")
        except Exception as e:
            logger.exception("-------- DELETING PID ERROR ------------")
            logger.exception(traceback.format_exc())


class IrokoAggs:

    @staticmethod
    def getAgg(query: dict):
        """
        devuelve los terminos de una agregacion.
        """
        # "query":{"query_string":{"query":"mayor"}
        # {"bool": {"filter": [{"terms": {"keywords": ["Cuba"]}}]}}}
        example_query = {
            "index": "records",
            "filters": [
                {"key": "keywords", "value": ["Cuba", "Covid"]},
                {"key": "creators", "value": ["Rafael Pila Peláez"]}
                ],
            "agg": {
                "filter": "creators",
                "size": 10000,
                }
            }

        assert query
        assert query["index"]
        assert query["agg"]
        query_size = query["agg"]["size"]
        query_index = query["index"]
        query_filter = query["agg"]["filter"]
        logger.info("-------------------------------------")
        logger.info("query_index: {0}    query_filter: {1}".format(query_index, query_filter))
        logger.info("-------------------------------------")
        filters = query["filters"]
        facets = current_app.config["RECORDS_REST_FACETS"]

        query_filters = []
        if query["filters"] and len(query["filters"]) > 0:
            for f in filters:
                field = facets[query_index]['aggs'][f['key']]['terms']['field']

                query_filters.append(
                    {"terms": {field: f['value']}}
                    )
        query_field = facets[query_index]['aggs'][query['agg']['filter']]['terms']['field']
        client = connections.create_connection(hosts=current_app.config["SEARCH_ELASTIC_HOSTS"])
        if len(query_filters) > 0:
            query_body = {
                "size": 0,
                "query": {
                    "bool": {
                        "filter": query_filters
                        }
                    },
                "aggs": {
                    query_filter: {
                        "terms": {
                            "field": query_field,
                            "size": query_size
                            }
                        }
                    }
                }
        else:
            query_body = {
                "size": 0,
                "aggs": {
                    query_filter: {
                        "terms": {
                            "field": query_field,
                            "size": query_size
                            }
                        }
                    }
                }
        logger.info("query_body: {0}".format(query_body))

        s = Search(using=client, index=query_index).update_from_dict(query_body)
        # search[0:offset].execute()
        t = s.execute()
        # # print(t.aggregations.sources.buckets)
        # return t.aggregations.sources.buckets
        result = []

        for item in t.aggregations[query_filter].buckets:
            # item.key will the house number
            result.append(
                {
                    'key': item.key,
                    'doc_count': item.doc_count
                    }
                )
        logger.info("return: {0}".format(result))
        return result
