# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 UPR.
#
# documents is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import DateString, SanitizedUnicode
from marshmallow import fields, missing, validate


def get_docid(obj, context):
    """Get record id."""
    pid = context.get('pid')
    return pid.pid_value if pid else missing


class PersonIdsSchemaV1(StrictKeysMixin):
    """Ids schema."""

    source = fields.Str()
    value = fields.Str()

class ReferenceSchemaV1(StrictKeysMixin):
    raw_reference = fields.Str()

class CreatorSchemaV1(StrictKeysMixin):
    """Contributor schema."""

    ids = fields.Nested(PersonIdsSchemaV1, many=True)
    name = fields.Str(required=True)
    affiliations = fields.List(fields.Str())
    email = fields.Str()

class ContributorSchemaV1(StrictKeysMixin):
    """Contributor schema."""

    ids = fields.Nested(PersonIdsSchemaV1, many=True)
    name = fields.Str(required=True)
    affiliations = fields.List(fields.Str())
    email = fields.Str()
    role = fields.Str()

class MetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    def get_docid(self, obj):
        """Get record id."""
        pid = self.context.get('pid')
        return pid.pid_value if pid else missing

    docid = fields.Function(
        serialize=get_docid,
        deserialize=get_docid)
    original_identifier = fields.Str()
    source = fields.Str()
    source_url = fields.Str()
    title = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    keywords = fields.Nested(fields.Str(), many=True)
    description = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    language = fields.Str()
    publication_date = DateString()
    contributors = fields.Nested(ContributorSchemaV1, many=True)
    creators = fields.Nested(ContributorSchemaV1, many=True)
    creators = fields.Nested(ReferenceSchemaV1, many=True)


class RecordSchemaV1(StrictKeysMixin):
    """Record schema."""

    metadata = fields.Nested(MetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = fields.Function(
        serialize=get_docid,
        deserialize=get_docid)
