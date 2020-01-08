
from marshmallow import Schema, fields, ValidationError, pre_load
from iroko.sources.models import Source, SourceType, TermSources, SourceType
from invenio_records_rest.schemas.fields import DateString
from iroko.harvester.marshmallow import RepositorySchema

class TermSourcesSchema(Schema):
    term_id = fields.Int()
    sources_id = fields.Int()
    data = fields.Raw(many=False)

class SourceVersionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    source_id = fields.Int()
    comment = fields.Str()
    created_at = fields.DateTime()
    is_current = fields.Boolean()
    data = fields.Raw(many=False)


class BaseSourceSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(allow_none=False)
    source_type = fields.Str(allow_none=False)
    source_status = fields.Str(allow_none=True)

    terms = fields.List(fields.Nested(TermSourcesSchema))
    versions = fields.Nested(SourceVersionSchema, many=True)
    repository = fields.Nested(RepositorySchema)


class SourceSchema(BaseSourceSchema):
    data = fields.Raw(many=False, allow_none=False)


source_schema_many = SourceSchema(many=True)
source_schema = SourceSchema()

