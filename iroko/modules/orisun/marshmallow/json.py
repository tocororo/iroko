# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 UPR.
#
# orisun is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import DateString, SanitizedUnicode
from marshmallow import fields, missing, validate


def get_orid(obj, context):
    """Get record id."""
    pid = context.get('pid')
    return pid.pid_value if pid else missing

class ReferenceSchemaV1(StrictKeysMixin):
    """Sources References Schema"""

    name = fields.Str()
    url = fields.Str()

class ISSNSchemaV1(StrictKeysMixin):
    """ISSN schema"""

    printed = fields.Str()
    electronic = fields.Str()
    link = fields.Str()

class MetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    def get_orid(self, obj):
        """Get record id."""
        pid = self.context.get('pid')
        return pid.pid_value if pid else missing

    orid = fields.Function(
        serialize=get_orid,
        deserialize=get_orid)
    title = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    issn = fields.Nested(ISSNSchemaV1, , many=False)
    rnps = fields.Str()
    email = fields.Str()
    logo = fields.Str()
    seriadas_cubanas = fields.Str()
    source_category = fields.Str()
    institution = fields.Str()
    subjects = fields.Nested(fields.Str(), many=True)
    licence = fields.Str()
    year_start = DateString()
    year_end = DateString()
    keywords = fields.Nested(fields.Str(), many=True)
    referecences = fields.Nested(ReferenceSchemaV1, many=True)


class SourceSchemaV1(StrictKeysMixin):
    """Record schema."""

    metadata = fields.Nested(MetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = fields.Function(
        serialize=get_orid,
        deserialize=get_orid)
