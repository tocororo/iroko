#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Document fetchers."""

from invenio_pidstore.fetchers import FetchedPID

import iroko.pidstore.pids as pids
import iroko.pidstore.providers as providers
from iroko.pidstore.pids import identifiers_schemas


def iroko_uuid_fetcher(record_uuid, data):
    """Fetch a document's identifiers.

    :param record_uuid: The record UUID.
    :param data: The record metadata.
    :returns: A :data:`invenio_pidstore.fetchers.FetchedPID` instance.
    """
    # pid_field = current_app.config['PIDSTORE_RECID_FIELD']
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


def iroko_record_identifiers_fetcher(record_uuid, data, pid_type):
    assert data, "no data"
    assert pids.IDENTIFIERS_FIELD in data
    for schema in identifiers_schemas:
        if schema == pid_type:
            return FetchedPID(
                provider=providers.IrokoRecordsIdentifiersProvider,
                pid_type=pid_type,
                pid_value=data[pids.IDENTIFIERS_FIELD][schema]
            )


def iroko_source_uuid_fetcher(source_uuid, data):
    assert data, "no data"
    assert pids.SOURCE_UUID_FIELD in data, "no source uuid in data"
    return FetchedPID(
        provider=providers.IrokoSourceUUIDProvider,
        pid_type=pids.SOURCE_UUID_PID_TYPE,
        pid_value=str(data[pids.SOURCE_UUID_FIELD]),
    )

# # TODO: esto debia ser eliminado quitando la tabla Sources, pero es muy complejo en marzo del 2020
# def iroko_source_source_record_fetcher(record_uuid, data):
#     return FetchedPID(
#         provider=providers.IrokoSourceSourceRecordProvider,
#         pid_type=providers.IrokoSourceSourceRecordProvider.pid_type,
#         pid_value=providers.IrokoSourceSourceRecordProvider.get_pid_from_data(data=data)
#     )
