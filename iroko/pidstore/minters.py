
"""Iroko minters."""

from flask import current_app
import iroko.pidstore.providers as providers

def iroko_uuid_minter(record_uuid, data):
    """Mint loan identifiers."""
    assert 'id' not in data
    provider = providers.IrokoUUIDProvider.create(
        object_type='rec',
        object_uuid=record_uuid,
    )
    # pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    # print(str(data))
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

