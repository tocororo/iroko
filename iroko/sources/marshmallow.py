
from marshmallow import Schema, fields, ValidationError, pre_load
from iroko.sources.models import Source, SourcesType, TermSources
from invenio_records_rest.schemas.fields import DateString

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


class SourceSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str()
    source_type = fields.Str()
    data = fields.Nested(JournalSchema, many=False)

    repo_harvest_type = fields.Str()
    repo_harvest_endpoint = fields.Str()
    repo_last_harvest_run = DateString()
    repo_identifier = fields.Str()
    repo_metadata_formats = fields.Str(many=True)
    repo_status = fields.Str()
    repo_error_log = fields.Str()



sources_schema = SourceSchema(many=True, only=('id', 'uuid', 'name', 'source_type', 'harvest_type','harvest_endpoint'))

sources_schema_full = SourceSchema(many=True)
source_schema_full = SourceSchema()

journal_schema = JournalSchema()

term_source_schema = TermSourcesSchema()
