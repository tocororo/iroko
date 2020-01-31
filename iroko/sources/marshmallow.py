
from marshmallow import Schema, fields, ValidationError, pre_load, post_dump
from iroko.sources.models import Source, SourceVersion, SourceType, TermSources, SourceStatus
from invenio_records_rest.schemas.fields import DateString
from iroko.harvester.marshmallow import RepositorySchema
from sqlalchemy import desc, asc
from iroko.taxonomy.api import Terms
from iroko.taxonomy.marshmallow import term_node_schema

from marshmallow_enum import EnumField

class TermSourcesSchema(Schema):
    term_id = fields.Int()
    sources_id = fields.Int()
    data = fields.Raw(many=False)

    @post_dump
    def dump_term(self, termSource, **kwargs):
        # TODO: version_to_review is true cuando tiene una version con una fecha posterior a la version current.
        msg, term = Terms.get_term_by_id(termSource['term_id']);
        termSource['term'] = term_node_schema.dump_term_node(term, 0, 0)

        return termSource


# TODO: to replace by UserProfilesSchema
class IrokoUserSchema(Schema):
    email = fields.Str()

class SourceVersionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    source_id = fields.Int()
    comment = fields.Str()
    created_at = fields.DateTime()
    is_current = fields.Boolean()
    data = fields.Raw(many=False)
    reviewed = fields.Boolean()
    user = fields.Nested(IrokoUserSchema)


class BaseSourceSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(allow_none=False)

    # TODO: los valores que se serializan son source_status:
    # "SourceStatus.UNOFFICIAL" source_type: "SourceType.JOURNAL"
    # esto habria que hacerlo mejor...el tipo de fields no deberia ser Str
    source_type = EnumField(SourceType, allow_none=False)
    source_status = EnumField(SourceStatus, allow_none=True)

    terms = fields.List(fields.Nested(TermSourcesSchema))
    versions = fields.Nested(SourceVersionSchema, many=True)
    repository = fields.Nested(RepositorySchema)

    @post_dump
    def dump_need_review_version(self, source, **kwargs):
        # TODO: version_to_review is true cuando tiene una version con una fecha posterior a la version current.
        versions = SourceVersion.query.filter_by(source_id=source['id']).order_by(desc(SourceVersion.created_at)).first()
        if versions and not versions.is_current:
            source['version_to_review'] = True
        else:
            source['version_to_review'] = False

        return source



class SourceSchema(BaseSourceSchema):
    data = fields.Raw(many=False, allow_none=False)


source_schema_many = SourceSchema(many=True, exclude=['versions'])
source_schema = SourceSchema()
source_schema_no_versions = SourceSchema(exclude=['versions'])
source_version_schema = SourceVersionSchema()
source_version_schema_many = SourceVersionSchema(many=True)

