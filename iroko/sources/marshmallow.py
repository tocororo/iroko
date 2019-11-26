
from marshmallow import Schema, fields, ValidationError, pre_load
from iroko.sources.models import Source, SourceType, TermSources, SourceType
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


class SourceDataSchema(Schema):
    """SourceData Schema, independently of SourceType, this means that in the JSON in the database anything can be put, and in case of different source types different data fields will be in. Eg, issn is for journals but not for repositories, this means that in the repository tuple the json data will not have the issn, same for other fields. The idea to put all here is because marshmallow will parse data if the data exist. """

    title = fields.Str()
    description = fields.Str()
    url = fields.Url()
    terms = fields.List(fields.Int)
    issn = fields.Nested(ISSNSchema, many=False)
    rnps = fields.Str()
    email = fields.Str()
    logo = fields.Str()
    seriadas_cubanas = fields.Url()
    year_start = fields.DateTime()
    year_end = fields.DateTime()


class SourceVersionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    source_id = fields.Int()
    comment = fields.Str()
    created_at = fields.DateTime()
    is_current = fields.Boolean()
    data = fields.Nested(SourceDataSchema, many=False)


class SourceSchema(Schema):

    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str()
    source_type = fields.Str()
    source_status = fields.Str()

    data = fields.Nested(SourceDataSchema, many=False)

    versions = fields.Nested(SourceVersionSchema, many=True)

    repo_harvest_type = fields.Str()
    repo_harvest_endpoint = fields.Str()
    repo_last_harvest_run = DateString()
    repo_identifier = fields.Str()
    repo_metadata_formats = fields.Str(many=True)
    repo_status = fields.Str()
    repo_error_log = fields.Str()



source_schema_many = SourceSchema(many=True, only=('id', 'uuid', 'name', 'source_type', 'source_status','harvest_endpoint'))
source_schema = SourceSchema(only=('id', 'uuid', 'name', 'source_type', 'source_status','harvest_endpoint'))

source_schema_full_many_no_versions = SourceSchema(many=True, exclude=('versions'))
source_schema_full = SourceSchema()

source_data_schema = SourceDataSchema()

term_source_schema = TermSourcesSchema()
