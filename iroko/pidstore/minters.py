#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko minters."""

import iroko.pidstore.pids as pids
import iroko.pidstore.providers as providers

import uuid


def iroko_uuid_minter(pid_type=None, pid_value=None, object_type=None,
                      object_uuid=None, data=None):
    """Mint loan identifiers."""
    assert data
    if not pid_type:
        pid_type = pids.RECORD_PID_TYPE
    if not pid_value:
        pid_value = uuid.uuid4()
    if not object_type:
        object_type = pids.IROKO_OBJECT_TYPE
    if not object_uuid:
        object_uuid = uuid.uuid4()

    provider = providers.IrokoUUIDProvider.create(
        pid_type=pid_type,
        pid_value=pid_value,
        object_type=object_type,
        object_uuid=object_uuid
        )
    # pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    # # print(str(data))
    data[pids.IROKO_UUID_FIELD] = provider.pid.pid_value
    return provider.pid


def iroko_source_oai_minter(record_uuid, data):
    provider = providers.IrokoSourceOAIProvider.create(
        object_type='rec',
        object_uuid=record_uuid,
        data=data
        )
    return provider.pid


def iroko_record_identifiers_minter(uuid, data, object_type):
    prsIDs = providers.IrokoRecordsIdentifiersProvider.create_identifiers(
        object_type=object_type,
        object_uuid=uuid,
        data=data
        )
    return prsIDs


def iroko_source_uuid_minter(source_uuid, data):
    provider = providers.IrokoSourceUUIDProvider.create(
        object_type=pids.IROKO_OBJECT_TYPE,
        object_uuid=source_uuid,
        data=data
        )
    return provider.pid


def organization_uuid_minter(org_uuid, data):
    provider = providers.OrganizationUUIDProvider.create(
        object_type=pids.IROKO_OBJECT_TYPE,
        object_uuid=org_uuid,
        data=data
        )
    return provider.pid


def identifiers_minter(uuid, data, object_type):
    prsIDs = providers.IdentifiersProvider.create_identifiers(
        object_type=object_type,
        object_uuid=uuid,
        data=data
        )
    return prsIDs

# # TODO: esto debia ser eliminado quitando la tabla Sources, pero es muy complejo en marzo del 2020
# def iroko_source_source_record_minter(record_uuid, data):
#     provider = providers.IrokoSourceSourceRecordProvider.create(
#         object_type='rec',
#         object_uuid=record_uuid,
#         data=data
#     )
#     return provider.pid
