
from marshmallow import Schema, fields, ValidationError, pre_load, post_dump, pre_dump
from iroko.sources.models import Source, SourceVersion, SourceType, TermSources, SourceStatus
from invenio_records_rest.schemas.fields import DateString
from iroko.harvester.marshmallow import RepositorySchema
from sqlalchemy import desc, asc

from marshmallow_enum import EnumField
from iroko.sources.marshmallow.journal import journal_data_schema
from iroko.sources.marshmallow.base import source_data_schema, IrokoUserSchema, TermSourcesSchema, SourceDataSchema

class SourceVersionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    source_id = fields.Int()
    comment = fields.Str()
    created_at = fields.DateTime()
    is_current = fields.Boolean()
    data = fields.Nested(SourceDataSchema, many=False)
    reviewed = fields.Boolean()
    user = fields.Nested(IrokoUserSchema)

    @post_dump(pass_original=True)
    def fix_data_field(self, result, version:SourceVersion, **kwargs):

        if version.source.source_type == SourceType.JOURNAL:
            data = journal_data_schema.dump(version.data)
        else:
            data =source_data_schema.dump(version.data)
        result['data'] = data
        return result


class SourceSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(allow_none=False)

    source_type = EnumField(SourceType, allow_none=False)
    source_status = EnumField(SourceStatus, allow_none=True)

    term_sources = fields.List(fields.Nested(TermSourcesSchema))
    versions = fields.Nested(SourceVersionSchema, many=True)
    repository = fields.Nested(RepositorySchema)

    data = fields.Nested(SourceDataSchema, many=False)

    @post_dump(pass_original=True)
    def fix_data_field(self, result, source:Source, **kwargs):

        if source.source_type == SourceType.JOURNAL:
            data = journal_data_schema.dump(source.data)
        else:
            data =source_data_schema.dump(source.data)
        result['data'] = data
        return result

    @post_dump
    def dump_need_review_version(self, source, **kwargs):
        # TODO: version_to_review is true cuando tiene una version con una fecha posterior a la version current.
        versions = SourceVersion.query.filter_by(source_id=source['id']).order_by(desc(SourceVersion.created_at)).first()
        if versions and not versions.is_current:
            source['version_to_review'] = True
        else:
            source['version_to_review'] = False

        return source


class IssnSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    data = fields.Raw(many=False)


source_schema_many = SourceSchema(many=True, exclude=['versions'])
source_schema = SourceSchema()
source_schema_no_versions = SourceSchema(exclude=['versions'])

source_version_schema = SourceVersionSchema()
source_version_schema_many = SourceVersionSchema(many=True)
issn_schema = IssnSchema()

