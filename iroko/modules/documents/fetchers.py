
"""Document fetchers."""

from collections import namedtuple

from flask import current_app

from .providers import DocumentPidProvider

FetchedPID = namedtuple('FetchedPID', ['provider', 'pid_type', 'pid_value'])
"""A pid fetcher."""


def document_pid_fetcher(record_uuid, data):
    """Fetch a document's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    return FetchedPID(
        provider=DocumentPidProvider,
        pid_type=DocumentPidProvider.pid_type,
        pid_value=str(data[pid_field]),
    )
