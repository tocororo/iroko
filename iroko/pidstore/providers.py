#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko Providers."""

import uuid

from invenio_pidstore.errors import PIDAlreadyExists
from invenio_pidstore.models import PIDStatus, PersistentIdentifier
from invenio_pidstore.providers.base import BaseProvider
from invenio_records import Record
from sqlalchemy.exc import NoResultFound

import iroko.pidstore.pids as pids
from iroko.pidstore.pids import identifiers_schemas


class IrokoUUIDProvider(BaseProvider):
    """Document identifier provider."""

    pid_type = pids.RECORD_PID_TYPE
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name.
    The provider name is not recorded in the PID since the provider does not
    provide any additional features besides creation of record ids.
    """

    default_status = PIDStatus.REGISTERED
    """Record IDs are by default registered immediately.
    Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
    """

    object_type = pids.IROKO_OBJECT_TYPE,

    @classmethod
    def create(cls,  pid_type=None, pid_value=None, object_type=None,
               object_uuid=None, **kwargs):
        """Create a new record identifier from the depoist PID value."""
        pid_type = pid_type or cls.pid_type
        pid_value = pid_value or uuid.uuid4()
        object_type = object_type or cls.object_type
        object_uuid = object_uuid or uuid.uuid4()
        kwargs.setdefault('status', cls.default_status)
        return super(IrokoUUIDProvider, cls).create(
            pid_type=pid_type,
            pid_value=pid_value,
            object_type=object_type,
            object_uuid=object_uuid,
            **kwargs
            )


class IrokoSourceOAIProvider(BaseProvider):
    """Provider in the form of {Source.uuid}-{Item.oaiIdentifier}
    When a record is harvested using OAI-PMH, is allways from a valid Source inside iroko,
    meaning that the Source must have an UUID.
    All items must have an oai identifier, since is harvested used OAI-PMH.
    So the persistent identifier use the form {Source.uuid}-{Item.oaiIdentifier}
    When migrating data across different installations of iroko, this need to be taken into
    consideration.
    """

    pid_type = pids.RECORD_SOURCE_OAI_PID_TYPE
    """Type of persistent identifier."""

    default_status = PIDStatus.REGISTERED
    """Record IDs are by default registered immediately.
    Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
    """

    @classmethod
    def create(cls, object_type=None, object_uuid=None, data=None, **kwargs):
        """Create a new record identifier from the depoist PID value."""
        pid_value = cls.get_pid_from_data(data)
        if 'pid_value' not in kwargs:
            kwargs.setdefault('pid_value', pid_value)
        kwargs.setdefault('status', cls.default_status)
        return super(IrokoSourceOAIProvider, cls).create(
            object_type=object_type, object_uuid=object_uuid, **kwargs
            )

    @classmethod
    def get_pid_from_data(cls, data=None):
        assert data, "no data"
        assert 'source_repo' in data, "no source in data"
        assert 'uuid' in data['source_repo'], "no source uuid"

        oai_id = None
        for idf in data['identifiers']:
            if idf['idtype'] == 'oai':
                oai_id = idf['value']
        assert oai_id, "no oai in idenfitiers in data, or not value for it"

        return data['source_repo']['uuid'] + '-' + oai_id


class IrokoRecordsIdentifiersProvider(BaseProvider):
    default_status = PIDStatus.REGISTERED

    @classmethod
    def create_identifiers(cls, object_type=None, object_uuid=None, data=None, **kwargs):

        assert data, "no data"
        # print('@@@@@@@@', data)
        assert pids.IDENTIFIERS_FIELD in data
        # print('@@@@@@@@')
        # assert pids.IROKO_UUID_FIELD in data
        pIDs = []
        # provider = super(IrokoRecordsIdentifiersProvider, cls).create(
        #             pid_type=pids.SOURCE_UUID_PID_TYPE,
        #             pid_value=data[pids.IROKO_UUID_FIELD],
        #             object_type=object_type,
        #             object_uuid=object_uuid,
        #             status=cls.default_status,
        #             **kwargs
        #         )
        # pIDs.append(provider.pid)
        # print('@@@@@@@@')
        for ids in data[pids.IDENTIFIERS_FIELD]:
            if ids['idtype'] in identifiers_schemas:
                # print('@@@@@@@@', ids['idtype'], ids['value'])
                # kwargs.setdefault('pid_type', ids['idtype'])
                # kwargs.setdefault('pid_value', ids['value'])
                # kwargs.setdefault('status', cls.default_status)
                provider = super(IrokoRecordsIdentifiersProvider, cls).create(
                    pid_type=ids['idtype'],
                    pid_value=ids['value'],
                    object_type=object_type,
                    object_uuid=object_uuid,
                    **kwargs
                    )
                # print('@@@@@@@@', provider.pid)
                pIDs.append(provider.pid)
                # print('@@@@@@@@')
        return pIDs

    @classmethod
    def create_pid(
        cls, pid_type, pid_value, object_type=None, object_uuid=None, data=None, **kwargs
        ):
        assert data, "no data"
        assert pids.IDENTIFIERS_FIELD in data
        assert pid_type
        assert pid_type in identifiers_schemas
        assert pid_value
        provider = super(IrokoRecordsIdentifiersProvider, cls).create(
            pid_type=pid_type,
            pid_value=pid_value,
            object_type=object_type,
            object_uuid=object_uuid,
            **kwargs
            )
        return provider.pid


class IrokoSourceUUIDProvider(BaseProvider):
    """Document identifier provider."""

    pid_type = pids.SOURCE_UUID_PID_TYPE
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name.
    The provider name is not recorded in the PID since the provider does not
    provide any additional features besides creation of record ids.
    """

    default_status = PIDStatus.REGISTERED
    """Record IDs are by default registered immediately.
    Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
    """

    @classmethod
    def create(cls, object_type=None, object_uuid=None, data=None, **kwargs):
        assert data, "no data"
        assert pids.IROKO_UUID_FIELD in data

        # kwargs.setdefault('pid_type', pids.SOURCE_UUID_PID_TYPE)
        # kwargs.setdefault('pid_value', data[pids.IROKO_UUID_FIELD])
        # kwargs.setdefault('status', cls.default_status)

        return super(IrokoSourceUUIDProvider, cls).create(
            object_type=object_type,
            object_uuid=object_uuid,
            pid_type=pids.SOURCE_UUID_PID_TYPE,
            pid_value=data[pids.IROKO_UUID_FIELD],
            **kwargs
            )


class OrganizationUUIDProvider(BaseProvider):
    """Document identifier provider."""

    pid_type = pids.ORGANIZATION_PID_TYPE
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name.
    The provider name is not recorded in the PID since the provider does not
    provide any additional features besides creation of record ids.
    """

    default_status = PIDStatus.REGISTERED
    """Record IDs are by default registered immediately.
    Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
    """

    object_type = pids.IROKO_OBJECT_TYPE,

    @classmethod
    def create(cls,  pid_type=None, pid_value=None, object_type=None,
               object_uuid=None, **kwargs):
        """Create a new record identifier from the depoist PID value."""
        pid_type = pid_type or cls.pid_type
        pid_value = pid_value or uuid.uuid4()
        object_type = object_type or cls.object_type
        object_uuid = object_uuid or uuid.uuid4()
        kwargs.setdefault('status', cls.default_status)
        return super(OrganizationUUIDProvider, cls).create(
            pid_type=pid_type,
            pid_value=pid_value,
            object_type=object_type,
            object_uuid=object_uuid,
            **kwargs
            )


class PersonUUIDProvider(BaseProvider):
    """Document identifier provider."""

    pid_type = pids.PERSON_PID_TYPE
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name.
    The provider name is not recorded in the PID since the provider does not
    provide any additional features besides creation of record ids.
    """

    default_status = PIDStatus.REGISTERED
    """Record IDs are by default registered immediately.
    Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
    """

    object_type = pids.IROKO_OBJECT_TYPE,

    @classmethod
    def create(cls,  pid_type=None, pid_value=None, object_type=None,
               object_uuid=None, **kwargs):
        """Create a new record identifier from the depoist PID value."""
        pid_type = pid_type or cls.pid_type
        pid_value = pid_value or uuid.uuid4()
        object_type = object_type or cls.object_type
        object_uuid = object_uuid or uuid.uuid4()
        kwargs.setdefault('status', cls.default_status)
        return super(PersonUUIDProvider, cls).create(
            pid_type=pid_type,
            pid_value=pid_value,
            object_type=object_type,
            object_uuid=object_uuid,
            **kwargs
            )



class IdentifiersProvider(BaseProvider):
    default_status = PIDStatus.REGISTERED

    @classmethod
    def create_identifiers(cls, object_type=None, object_uuid=None, data=None,  **kwargs):

        assert data, "no data"
        assert pids.IDENTIFIERS_FIELD in data
        pIDs = []
        for ids in data[pids.IDENTIFIERS_FIELD]:
            if ids['idtype'] in identifiers_schemas:
                try:

                    provider = super(IdentifiersProvider, cls).create(
                        pid_type=ids['idtype'],
                        pid_value=ids['value'],
                        object_type=object_type,
                        object_uuid=object_uuid,
                        status=cls.default_status,
                        **kwargs
                    )
                    pIDs.append(provider.pid)
                except PIDAlreadyExists as ex:
                    pid: PersistentIdentifier = PersistentIdentifier.get(ids['idtype'],
                                                                         ids['value'])
                    obj_id = pid.get_assigned_object(object_type=object_type)
                    try:
                        obj = Record.get_record(obj_id)
                        raise ex
                    except NoResultFound:
                        # esto significa que el pid existe, pero no está asociado a ningun
                        # objeto, es decir, es un error, por tanto podemos actualizar el pid para
                        # el nuevo objeto.
                        if pid.assign(object_type=object_type, object_uuid=object_uuid,
                                      overwrite=True):
                            pIDs.append(pid)
                        else:
                            # TODO: delete pid?
                            raise ex


        return pIDs

    @classmethod
    def create_pid(cls, pid_type, object_type=None, object_uuid=None, data=None,  **kwargs):
        assert data, "no data"
        assert pids.IDENTIFIERS_FIELD in data
        assert pid_type
        assert pid_type in identifiers_schemas
        for ids in data[pids.IDENTIFIERS_FIELD]:
            if ids['idtype'] == pid_type:
                provider = super(IdentifiersProvider, cls).create(
                    pid_type=ids['idtype'],
                    pid_value=ids['value'],
                    object_type=object_type,
                    object_uuid=object_uuid,
                    status=cls.default_status,
                    **kwargs
                )
                return provider.pid



# class IrokoSourceSourceRecordProvider(BaseProvider):
#     """Provider to relate Iroko's table Source, with SourceRecord in invenio Records ."""
#     # TODO: esto debia ser eliminado quitando la tabla Sources, pero es muy complejo en marzo
#      del 2020

#     pid_type = pids.SOURCE_UUID_PID_TYPE

#     pid_provider = None

#     default_status = PIDStatus.REGISTERED

#     @classmethod
#     def create(cls, object_type=None, object_uuid=None, data=None, **kwargs):
#         """Create a new record identifier from the depoist PID value."""
#         pid_value = cls.get_pid_from_data(data)
#         kwargs.setdefault('pid_value', pid_value)
#         kwargs.setdefault('status', cls.default_status)
#         return super(IrokoSourceSourceRecordProvider, cls).create(
#             object_type=object_type, object_uuid=object_uuid, **kwargs)

#     @classmethod
#     def get_pid_from_data(cls, data=None):
#         assert data, "no data"
#         assert 'source_uuid' in data, "no source uuid in data"
#         return data['source_uuid']
