

from invenio_records_rest.loaders.marshmallow import marshmallow_loader
from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import PersistentIdentifier
from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import (
    record_responsify,
    search_responsify,
)
from marshmallow import fields

from iroko.sources.marshmallow.journal import JournalDataSchema


class SourceDataSchemaV1(JournalDataSchema):
    pass


class SourceSchemaV1(StrictKeysMixin):
    """Source schema."""

    metadata = fields.Nested(SourceDataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()

source_data_schema_many = SourceDataSchemaV1(many=True)

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
