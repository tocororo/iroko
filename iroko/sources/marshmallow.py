
from marshmallow import Schema, fields, ValidationError, pre_load
from iroko.sources.models import Sources, SourcesType, TermSources

# class TermSourcesMetadataSchema(Schema):

class ReferenceSchema(Schema):
    url = fields.Url()

class TermSourcesSchema(Schema):
    term_id = fields.Int(dump_only=True)
    sources_id = fields.Int(dump_only=True)
    # data = fields.Nested(TermSourcesMetadataSchema)

class ISSNSchema(Schema):
    p = fields.Str()
    e = fields.Str()
    l = fields.Str()


class SourcesDataSchema(Schema):
    description = fields.Str()
    url = fields.Url()

class JournalSchema(SourcesDataSchema):

    issn = fields.Nested(ISSNSchema, many=False)
    rnps = fields.Str()
    email = fields.Str()
    logo = fields.Str()
    seriadas_cubanas = fields.Url()
    year_start = fields.DateTime()
    year_end = fields.DateTime()


class SourcesSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str()
    source_type = fields.Str()
    data = fields.Nested(JournalSchema, many=False)
    harvest_type = fields.Str()
    harvest_endpoint = fields.Url()



sources_schema = SourcesSchema(many=True, only=('id', 'uuid', 'name', 'source_type', 'harvest_type','harvest_endpoint'))

sources_schema_full = SourcesSchema(many=True)
source_schema_full = SourcesSchema()

journal_schema = JournalSchema()

term_source_schema = TermSourcesSchema()
