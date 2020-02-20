
from marshmallow import Schema, fields, ValidationError, pre_load, post_dump
from iroko.sources.models import Source, SourceVersion, SourceType, TermSources, SourceStatus
from invenio_records_rest.schemas.fields import DateString
from iroko.harvester.marshmallow import RepositorySchema
from sqlalchemy import desc, asc
from iroko.taxonomy.api import Terms
from iroko.taxonomy.marshmallow import term_schema

from marshmallow_enum import EnumField



class TermSourcesSchema(Schema):
    term_id = fields.Int()
    sources_id = fields.Int()
    data = fields.Raw(many=False)

    @post_dump
    def dump_term(self, termSource, **kwargs):
        # TODO: version_to_review is true cuando tiene una version con una fecha posterior a la version current.
        msg, term = Terms.get_term_by_id(termSource['term_id'])
        termSource['term'] = term_schema.dump(term)

        return termSource

class SourceDataSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    term_sources = fields.List(fields.Nested(TermSourcesSchema))



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
    data = fields.Nested(SourceDataSchema, many=False)
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

    term_sources = fields.List(fields.Nested(TermSourcesSchema))
    versions = fields.Nested(SourceVersionSchema, many=True)
    repository = fields.Nested(RepositorySchema)

    # @post_dump
    # def temp_term_sources(self, source, **kwargs):
    #     # TODO: cambiar en TermSource sources/models.py, el backref, y quitar esta funcion
    #     # cambiar el campo terms por term_sources aqui y en el modelo
    #     # source = db.relationship("Source", backref=db.backref("terms"))
    #     # source['term_sources'] = source['terms']

    #     # el valor que hay en el data siempre tiene que ser el mismo que en la fuente. 
    #     source['data']['term_sources'] = source['term_sources']
    #     return source

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
    data = fields.Nested(SourceDataSchema, many=False)

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

