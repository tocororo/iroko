# -*- coding: utf-8 -*-

#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_records_rest.schemas import Nested, StrictKeysMixin
from invenio_records_rest.schemas.fields import (
    DateString,
    PersistentIdentifier, SanitizedUnicode,
)
from marshmallow import fields, missing, validate, post_dump

from iroko.sources.marshmallow.base import OrganizationDataSchema, ClasificationDataSchema


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


class ContributorSchemaV1(StrictKeysMixin):
    """Contributor schema."""

    ids = fields.Nested(PersonIdsSchemaV1, many=True)
    name = SanitizedUnicode(required=True)
    affiliations = fields.List(SanitizedUnicode())
    email = fields.Email()
    roles = fields.List(SanitizedUnicode())

    @post_dump
    def no_email(self, contributor):
        contributor['email'] = ''
        return contributor


class IdentifierSchemaV1(StrictKeysMixin):
    """Ids schema."""

    idtype = SanitizedUnicode()
    value = SanitizedUnicode()


class SourceSchemaV1(StrictKeysMixin):
    uuid = fields.Str()
    name = SanitizedUnicode()


class SpecSchemaV1(StrictKeysMixin):
    code = fields.Str()
    name = SanitizedUnicode(validate=validate.Length(min=3))


class MetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    id = PersistentIdentifier()
    identifiers = Nested(IdentifierSchemaV1, many=True)
    source_repo = Nested(SourceSchemaV1)
    spec = Nested(SpecSchemaV1)
    title = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    creators = Nested(ContributorSchemaV1, many=True)
    keywords = fields.List(SanitizedUnicode(), many=True)
    description = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    publisher = SanitizedUnicode()
    sources = fields.List(SanitizedUnicode(), many=True)
    rights = fields.List(SanitizedUnicode(), many=True)
    types = fields.List(SanitizedUnicode(), many=True)
    formats = fields.List(SanitizedUnicode(), many=True)
    language = fields.Str()
    publication_date = DateString()
    contributors = Nested(ContributorSchemaV1, many=True)
    references = Nested(ReferenceSchemaV1, many=True)
    terms = fields.List(SanitizedUnicode(), many=True)
    status = fields.Str()
    organizations = Nested(OrganizationDataSchema, many=True)
    classifications = Nested(ClasificationDataSchema, many=True)


class RecordSchemaV1(StrictKeysMixin):
    """Record schema."""

    metadata = fields.Nested(MetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()
