# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# Iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_jsonschemas import current_jsonschemas
from invenio_records_rest.schemas import Nested, StrictKeysMixin
from invenio_records_rest.schemas.fields import (
    DateString, GenFunction,
    PersistentIdentifier, SanitizedUnicode,
    )
from marshmallow import fields, missing, validate, post_dump, INCLUDE

allow_empty = validate.Length(min=0)


def bucket_from_context(_, context):
    """Get the record's bucket from context."""
    record = (context or {}).get('record', {})
    return record.get('_bucket', missing)


def files_from_context(_, context):
    """Get the record's files from context."""
    record = (context or {}).get('record', {})
    return record.get('_files', missing)


def schema_from_context(_, context):
    """Get the record's schema from context."""
    record = (context or {}).get('record', {})
    return record.get(
        "_schema",
        current_jsonschemas.path_to_url(PersonRecord._schema)
    )


class IdentifierSchemaV1(StrictKeysMixin):
    """Ids schema."""

    idtype = SanitizedUnicode()
    value = SanitizedUnicode()


class CountrySchemaV1(StrictKeysMixin):
    name = SanitizedUnicode()
    code = SanitizedUnicode()


class AffiliationSchemaV1(StrictKeysMixin):
    id = SanitizedUnicode()
    identifiers = Nested(IdentifierSchemaV1, many=True, required=True)
    start_date  = DateString()
    end_date = DateString()
    label = SanitizedUnicode()
    roles = fields.List(SanitizedUnicode(), many=True)


class PublicationSchemaV1(StrictKeysMixin):
    id = SanitizedUnicode()
    identifiers = Nested(IdentifierSchemaV1, many=True, required=True)
    title = SanitizedUnicode()
    roles = fields.List(SanitizedUnicode(), many=True)
    status = fields.List(SanitizedUnicode(), many=True)


class SourceSchemaV1(StrictKeysMixin):
    id = SanitizedUnicode()
    identifiers = Nested(IdentifierSchemaV1, many=True, required=True)
    name = SanitizedUnicode()
    roles = fields.List(SanitizedUnicode(), many=True)


class PersonMetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    id = PersistentIdentifier()
    identifiers = Nested(IdentifierSchemaV1, many=True, required=True)
    name = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    last_name = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    public = fields.Bool()
    active = fields.Bool()
    gender = SanitizedUnicode()
    country = Nested(CountrySchemaV1, many=False)
    email_addresses = fields.List(SanitizedUnicode(), validate=validate.Email())
    aliases = fields.List(SanitizedUnicode(), many=True)
    research_interests = fields.List(SanitizedUnicode(), many=True)
    key_words = fields.List(SanitizedUnicode(), many=True)
    academic_titles = fields.List(SanitizedUnicode(), many=True)
    affiliations = Nested(AffiliationSchemaV1, many=True)
    roles_sceiba = fields.List(SanitizedUnicode(), many=True)
    publications = Nested(PublicationSchemaV1, many=True)
    sources = Nested(SourceSchemaV1, many=True)
    _schema = GenFunction(
        attribute="$schema",
        data_key="$schema",
        deserialize=schema_from_context,  # to be added only when loading
    )


class PersonRecordSchemaV1(StrictKeysMixin):
    """Record schema."""

    metadata = fields.Nested(PersonMetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()
    files = GenFunction(
        serialize=files_from_context, deserialize=files_from_context)

personMetadataSchema = PersonMetadataSchemaV1(many=False, unknown=INCLUDE)
