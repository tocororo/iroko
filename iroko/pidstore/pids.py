# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from invenio_pidstore.errors import PIDAlreadyExists, PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier

"""Iroko App PIDs."""

RECORD_SOURCE_OAI_PID_TYPE = "recoai"

IDENTIFIERS_FIELD = "identifiers"
IDENTIFIERS_FIELD_TYPE = "idtype"
IDENTIFIERS_FIELD_VALUE = "value"

RECORD_PID_TYPE = "irouid"
RECORD_PID_MINTER = "irouid"
RECORD_PID_FETCHER = "irouid"


SOURCE_UUID_PID_TYPE = "srcid"
SOURCE_UUID_PID_MINTER = "srcid"
SOURCE_UUID_PID_FETCHER = "srcid"
SOURCE_UUID_FIELD = "id"
SOURCE_TYPE = "rec"

ORGANIZATION_PID_TYPE = "orgid"
ORGANIZATION_PID_MINTER = "orgid"
ORGANIZATION_PID_FETCHER = "orgid"
ORGANIZATION_PID_FIELD = "id"
ORGANIZATION_TYPE = "rec"


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
                pid = PersistentIdentifier.get(
                    ids[IDENTIFIERS_FIELD_TYPE], ids[IDENTIFIERS_FIELD_VALUE]
                    )
                return pid
            except Exception:
                pass
    return None


def check_data_identifiers(data):
    """
    check if identifiers field is present in data, and then check if any on the PIDs
    not exists...
    """
    # # print('IDENTIFIERS_FIELD in data {0}'.format(data))
    assert IDENTIFIERS_FIELD in data
    # # print(data)
    for ids in data[IDENTIFIERS_FIELD]:
        if ids[IDENTIFIERS_FIELD_TYPE] in identifiers_schemas:
            try:
                pid = PersistentIdentifier.get(
                    ids[IDENTIFIERS_FIELD_TYPE], ids[IDENTIFIERS_FIELD_VALUE]
                    )
                raise PIDAlreadyExists(
                    pid_type=ids[IDENTIFIERS_FIELD_TYPE], pid_value=ids[IDENTIFIERS_FIELD_VALUE]
                    )
            except PIDDoesNotExistError:
                pass
    return True


identifiers_schemas = [
    "ark",
    "arxiv",
    "doi",
    "bibcode",
    "ean8",
    "ean13",
    "handle",
    "isbn",
    "issn_l",
    "issn_p",
    "issn_e",
    "issn_c",
    "issn_o",
    "istc",
    "lsid",
    "pmid",
    "pmcid",
    "purl",
    "upc",
    "url",
    "urn",
    "orcid",
    "gnd",
    "ads",
    "oai",
    "prnps",
    "ernps",
    "oaiurl",
    "grid",
    "wkdata",
    "ror",
    "isni",
    "fudref",
    "orgref",
    "reup",
    "grid",
    "wkdata",
    "ror",
    "isni",
    "fudref",
    "orgref",
    "reup",
    "orgaid",
    "uniid",
    "sceibaid"
    ]


def get_identifier_schema(pid):
    for schema in identifiers_schemas:
        if schema in pid:
            return schema
    if 'http' in pid or 'https' in pid:
        return 'url'
    return None
