# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# Iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Schemas for marshmallow."""

from __future__ import absolute_import, print_function

from .json import MetadataSchemaV1, MetadataSchemaRelIDsV1, RecordSchemaV1, RecordSearchSchemaV1, MetadataSchemaBaseV1

__all__ = ('MetadataSchemaV1', 'MetadataSchemaRelIDsV1' , 'RecordSchemaV1', 'RecordSearchSchemaV1', 'MetadataSchemaBaseV1')
