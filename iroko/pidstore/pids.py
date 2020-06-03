# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 UPR.
#

from invenio_pidstore.errors import PIDDoesNotExistError, PIDAlreadyExists
from invenio_pidstore.models import PersistentIdentifier

from iroko.utils import identifiers_schemas

"""Iroko App PIDs."""

RECORD_PID_TYPE = "irouid"
"""Persistent Identifier for Source."""
RECORD_PID_MINTER = "irouid"
"""Minter PID for Source."""
RECORD_PID_FETCHER = "irouid"
"""Fetcher PID for Source."""

ORGANIZATION_PID_TYPE = "orgid"
ORGANIZATION_PID_MINTER = "orgid"
ORGANIZATION_PID_FETCHER = "orgid"
ORGANIZATION_PID_FIELD = "id"
ORGANIZATION_TYPE = "org"

RECORD_SOURCE_OAI_PID_TYPE = "recoai"


IDENTIFIERS_FIELD = "identifiers"
IDENTIFIERS_FIELD_TYPE = "idtype"
IDENTIFIERS_FIELD_VALUE = "value"

SOURCE_UUID_FIELD = "source_uuid"

SOURCE_TYPE = "src"

SOURCE_UUID_PID_TYPE = "srcid"
"""Persistent Identifier for Source."""
SOURCE_UUID_PID_MINTER = "srcid"
"""Minter PID for Source."""
SOURCE_UUID_PID_FETCHER = "srcid"
"""Fetcher PID for Source."""


def get_pid_by_data(data):
    """
    get pid or none,
    seek the IDENTIFIERS_FIELD in data, and then try to get PersistentIdentifier
    using any IDENTIFIERS_FIELD_TYPE, if a PID is found is returned
    else return None
    """
    assert IDENTIFIERS_FIELD in data
    for ids in data[IDENTIFIERS_FIELD]:
        if ids[IDENTIFIERS_FIELD_TYPE] in identifiers_schemas:
            try:
                pid = PersistentIdentifier.get(ids[IDENTIFIERS_FIELD_TYPE], ids[IDENTIFIERS_FIELD_VALUE])
                return pid
            except Exception:
                pass
    return None

def check_data_identifiers(data):
    """
    check if identifiers field is present in data, and then check if any on the PIDs
    not exists...
    """
    # print('IDENTIFIERS_FIELD in data {0}'.format(data))
    assert IDENTIFIERS_FIELD in data
    # print(data)
    for ids in data[IDENTIFIERS_FIELD]:
        if ids[IDENTIFIERS_FIELD_TYPE] in identifiers_schemas:
            try:
                pid = PersistentIdentifier.get(ids[IDENTIFIERS_FIELD_TYPE], ids[IDENTIFIERS_FIELD_VALUE])
                raise PIDAlreadyExists(pid_type=ids[IDENTIFIERS_FIELD_TYPE], pid_value=ids[IDENTIFIERS_FIELD_VALUE])
            except PIDDoesNotExistError:
                pass
    return True
