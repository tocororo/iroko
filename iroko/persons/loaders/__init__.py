# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# Iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Loaders.

This file contains sample loaders that can be used to deserialize input data in
an application level data structure. The marshmallow_loader() method can be
parameterized with different schemas for the record metadata. In the provided
json_v1 instance, it uses the MetadataSchemaV1, defining the
PersistentIdentifier field.
"""

from __future__ import absolute_import, print_function

from invenio_records_rest.loaders.marshmallow import marshmallow_loader

from iroko.persons.marshmallow import PersonRecordSchemaV1

#: JSON loader using Marshmallow for data validation.
json_v1 = marshmallow_loader(PersonRecordSchemaV1)

__all__ = (
    'json_v1',
)
