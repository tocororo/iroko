
"""Iroko minters."""

from flask import current_app
from .providers import IrokoUUIDProvider


def iroko_uuid_minter(record_uuid, data):
    """Mint loan identifiers."""
    assert 'id' not in data
    provider = IrokoUUIDProvider.create(
        object_type='rec',
        object_uuid=record_uuid,
    )
    # pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    print(str(data))
    pid_field = 'id'
    data[pid_field] = provider.pid.pid_value
    return provider.pid
