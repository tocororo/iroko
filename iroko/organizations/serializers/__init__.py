# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# Iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Record serializers."""

from __future__ import absolute_import, print_function

from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import (
    record_responsify,
    search_responsify,
)

from iroko.organizations.marshmallow import RecordSearchSchemaV1, MetadataSchemaBaseV1
from ..marshmallow import RecordSchemaV1

# Serializers
# ===========
#: JSON serializer definition.
json_v1 = JSONSerializer(RecordSchemaV1, replace_refs=True)
org_json_v1 = JSONSerializer(MetadataSchemaBaseV1, replace_refs=True)
json_v1_for_search = JSONSerializer(RecordSearchSchemaV1, replace_refs=True)

# Records-REST serializers
# ========================
#: JSON record serializer for individual organizations.
json_v1_response = record_responsify(json_v1, 'application/json')
#: JSON record serializer for search results.
json_v1_search = search_responsify(json_v1_for_search, 'application/json')

__all__ = (
    'json_v1',
    'json_v1_for_search',
    'json_v1_response',
    'json_v1_search',
)
