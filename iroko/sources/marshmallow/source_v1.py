#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
import typing

from invenio_records_rest.loaders.marshmallow import marshmallow_loader
from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import PersistentIdentifier
from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import (
    record_responsify,
    search_responsify,
    )
from marshmallow import Schema, fields

from iroko.sources.marshmallow.base import SourceDataSchema
from iroko.sources.marshmallow.journal import JournalDataSchema
from iroko.sources.models import SourceType


class SourceDataSchemaV1(Schema):

    def load(self, data, *, many=None, partial=None, unknown=None, **kwargs):
        if data['source_type'] == SourceType.JOURNAL.value:
            journal = JournalDataSchema()
            print('RRRRRRRRRRRRR load JOURNAL RRRRRRRRRRRRRRRRRRRRrr')
            return journal.load(data, many, partial, unknown, **kwargs)
        else:
            source = SourceDataSchema()
            print('QAAAAAAAAAAAA load SOURCE AAAAAAAAAAAAAAAAAAAAAAAAa')
            return source.load(data, many, partial, unknown, **kwargs)
        return self.load(data, many, partial, unknown, **kwargs)

    def dump(self, obj: typing.Any, *, many: typing.Optional[bool] = None):
        many = self.many if many is None else bool(many)
        if many:
            return self.dump(obj)
        else:
            if obj['source_type'] == SourceType.JOURNAL.value:
                journal = JournalDataSchema(many=False)
                print('RRRRRRRRRRR dump JOURNAL RRRRRRRRRRRRRRRRRRRRRRrr')
                return journal.dump(obj)
            else:
                print('QAAAAAAAAAAAA dump SOURCE AAAAAAAAAAAAAAAAAAAAAAAAa')
                source = SourceDataSchema(many=False)
                return source.dump(obj)


class SourceSchemaV1(StrictKeysMixin):
    """Source schema."""

    metadata = fields.Nested(SourceDataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()

    # @post_dump
    # def dump_metadata(self, source, **kwargs):
    #     if source['metadata']['source_type'] == SourceType.JOURNAL.value:
    #         print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsss')
    #         print(source)
    #         print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsss')
    #         source['metadata'] = journal_data_schema.dump(source['metadata'])
    #     return source


source_data_schema_many = SourceDataSchemaV1(many=True)
source_data_schema = SourceDataSchemaV1(many=False)

source_loader_v1 = marshmallow_loader(SourceDataSchemaV1)

# Serializers
# ===========
#: JSON serializer definition.
source_v1 = JSONSerializer(SourceSchemaV1, replace_refs=True)

# Records-REST serializers
# ========================
#: JSON record serializer for individual records.
source_v1_response = record_responsify(source_v1, 'application/json')
#: JSON record serializer for search results.
source_v1_search = search_responsify(source_v1, 'application/json')
