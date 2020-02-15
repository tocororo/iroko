
"""Document fetchers."""

from collections import namedtuple

from flask import current_app

import iroko.pidstore.providers as providers

FetchedPID = namedtuple('FetchedPID', ['provider', 'pid_type', 'pid_value'])
"""A pid fetcher."""


def iroko_uuid_fetcher(record_uuid, data):
    """Fetch a document's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    # pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    # print(str(data))
    pid_field = 'id'
    return FetchedPID(
        provider=providers.IrokoUUIDProvider,
        pid_type=providers.IrokoUUIDProvider.pid_type,
        pid_value=str(data[pid_field]),
    )


def iroko_source_oai_fetcher(record_uuid, data):
    return FetchedPID(
        provider=providers.IrokoSourceOAIProvider,
        pid_type=providers.IrokoSourceOAIProvider.pid_type,
        pid_value=providers.IrokoSourceOAIProvider.get_pid_from_data(data=data)
    )
