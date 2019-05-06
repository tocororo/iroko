# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 UPR.
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_records_rest.schemas import Nested, StrictKeysMixin
from invenio_records_rest.schemas.fields import DateString, \
    PersistentIdentifier, SanitizedUnicode
from marshmallow import fields, missing, validate


def get_recid(obj, context):
    """Get record id."""
    pid = context.get('pid')
    return pid.pid_value if pid else missing



class PersonIdsSchemaV1(StrictKeysMixin):
    """Ids schema."""

    source = SanitizedUnicode()
    value = SanitizedUnicode()

class ReferenceSchemaV1(StrictKeysMixin):
    # use SanitizedUnicode()?
    raw_reference = fields.Str()


class CreatorSchemaV1(StrictKeysMixin):
    """Contributor schema."""

    ids = fields.Nested(PersonIdsSchemaV1, many=True)
    name = SanitizedUnicode(required=True)
    role = SanitizedUnicode()
    affiliations = fields.List(SanitizedUnicode())
    email = fields.Email()


class ContributorSchemaV1(StrictKeysMixin):
    """Contributor schema."""

    ids = fields.Nested(PersonIdsSchemaV1, many=True)
    name = SanitizedUnicode(required=True)
    role = SanitizedUnicode()
    affiliations = fields.List(SanitizedUnicode())
    email = fields.Email()  
    role = SanitizedUnicode()


class MetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    # id = PersistentIdentifier()
    recid = fields.Function(serialize=get_recid, deserialize=get_recid)
    original_identifier = fields.Str()
    source = fields.Str()
    sourceSet = fields.Str()
    spec = SanitizedUnicode(validate=validate.Length(min=3))
    identifiers = fields.List(fields.Str(), many=True)
    title = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    keywords = fields.List(SanitizedUnicode(), many=True)
    description = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    language = fields.Str()
    publication_date = DateString()
    contributors = Nested(ContributorSchemaV1, many=True)
    creators = Nested(CreatorSchemaV1, many=True)
    references = Nested(ReferenceSchemaV1, many=True)


class RecordSchemaV1(StrictKeysMixin):
    """Record schema."""

    metadata = fields.Nested(MetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    # id = PersistentIdentifier()
    id = fields.Function(
        serialize=get_recid,
        deserialize=get_recid)
