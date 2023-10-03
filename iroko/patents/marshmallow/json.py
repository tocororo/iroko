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
from marshmallow import INCLUDE, fields, missing, validate

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
        current_jsonschemas.path_to_url(PatentRecord._schema)
    )


class IdentifierSchemaV1(StrictKeysMixin):
    """Ids schema."""

    idtype = SanitizedUnicode()
    value = SanitizedUnicode()


class CountrySchemaV1(StrictKeysMixin):
    name = SanitizedUnicode()
    code = SanitizedUnicode()


class AffiliationsSchemaV1(StrictKeysMixin):
    id = SanitizedUnicode()
    identifiers = Nested(IdentifierSchemaV1, many=True, required=True)
    name = SanitizedUnicode()

class PersonSchemaV1(StrictKeysMixin):
    id = SanitizedUnicode()
    identifiers = Nested(IdentifierSchemaV1, many=True, required=True)
    name = SanitizedUnicode()


class PatentMetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    id = PersistentIdentifier()
    identifiers = Nested(IdentifierSchemaV1, many=True, required=True)
    title = SanitizedUnicode(required=True, validate=validate.Length(min=3))
    authors = Nested(PersonSchemaV1, many=True)
    affiliations = Nested(AffiliationsSchemaV1, many=True)
    co_author = Nested(PersonSchemaV1, many=True)
    summary = SanitizedUnicode()
    classification = SanitizedUnicode()
    claims = SanitizedUnicode()
    prior_art = SanitizedUnicode()
    drawing = SanitizedUnicode()
    countries = fields.List(SanitizedUnicode(), many=True)
    country = Nested(CountrySchemaV1, many=False)
    international = fields.Bool()
    expedient_number = SanitizedUnicode()
    key_words = fields.List(SanitizedUnicode(), many=True)
    presentation_date = DateString()
    register_number = SanitizedUnicode()
    register_date = DateString()
    publication_date = DateString()
    ipc_clases = SanitizedUnicode()
    subtype = SanitizedUnicode()
    legal_status = SanitizedUnicode()
    _schema = GenFunction(
        attribute="$schema",
        data_key="$schema",
        deserialize=schema_from_context,  # to be added only when loading
    )


class PatentRecordSchemaV1(StrictKeysMixin):
    """Record schema."""

    metadata = fields.Nested(PatentMetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()
    files = GenFunction(
        serialize=files_from_context, deserialize=files_from_context)

patentMetadataSchema = PatentMetadataSchemaV1(many=False, unknown=INCLUDE)
