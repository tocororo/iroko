

from invenio_records_rest.loaders.marshmallow import marshmallow_loader

from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import record_responsify, \
    search_responsify

from invenio_records_rest.schemas import StrictKeysMixin


from iroko.records.marshmallow.json import IdentifierSchemaV1
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from iroko.sources.marshmallow.journal import JournalDataSchema
from iroko.sources.marshmallow.source import SourceType, SourceStatus
from invenio_records_rest.schemas.fields import DateString, \
    PersistentIdentifier, SanitizedUnicode

class RelationSchemaV1(Schema):
    uuid = fields.UUID(dump_only=True)
    data = fields.Raw(many=False)

class SourceDataSchemaV1(JournalDataSchema):

    id = PersistentIdentifier()
    source_uuid = fields.UUID(dump_only=True)
    identifiers = fields.Nested(IdentifierSchemaV1, many=True)
    name = fields.Str(allow_none=False)

    source_type = fields.Str(allow_none=False)
    source_status = fields.Str(allow_none=True)

    relations = fields.List(fields.Nested(RelationSchemaV1))



class SourceSchemaV1(StrictKeysMixin):
    """Source schema."""

    metadata = fields.Nested(SourceDataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()


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
