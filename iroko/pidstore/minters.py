
"""Iroko minters."""

import iroko.pidstore.pids as pids
import iroko.pidstore.providers as providers



def iroko_uuid_minter(record_uuid, data):
    """Mint loan identifiers."""
    assert 'id' not in data
    provider = providers.IrokoUUIDProvider.create(
        object_type='rec',
        object_uuid=record_uuid,
    )
    # pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    # # print(str(data))
    pid_field = 'id'
    data[pid_field] = provider.pid.pid_value
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
        object_type=pids.SOURCE_TYPE,
        object_uuid=source_uuid,
        data=data
    )
    return provider.pid



# # TODO: esto debia ser eliminado quitando la tabla Sources, pero es muy complejo en marzo del 2020
# def iroko_source_source_record_minter(record_uuid, data):
#     provider = providers.IrokoSourceSourceRecordProvider.create(
#         object_type='rec',
#         object_uuid=record_uuid,
#         data=data
#     )
#     return provider.pid

