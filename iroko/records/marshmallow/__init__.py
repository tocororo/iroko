# -*- coding: utf-8 -*-

#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Schemas for marshmallow."""

from __future__ import absolute_import, print_function

from .json import MetadataSchemaV1, RecordSchemaV1, RecordFullSchemaV1, MetadataFullSchemaV1

__all__ = ('MetadataSchemaV1', 'RecordSchemaV1', 'RecordFullSchemaV1', 'MetadataFullSchemaV1')
