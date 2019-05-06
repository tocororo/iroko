
"""Document fetchers."""

from collections import namedtuple

from flask import current_app

from .providers import IrokoRecordsPidProvider

FetchedPID = namedtuple('FetchedPID', ['provider', 'pid_type', 'pid_value'])
"""A pid fetcher."""


def record_pid_fetcher(record_uuid, data):
    """Fetch a document's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    return FetchedPID(
        provider=IrokoRecordsPidProvider,
        pid_type=IrokoRecordsPidProvider.pid_type,
        pid_value=str(data[pid_field]),
    )
