

from marshmallow import Schema, fields, ValidationError, pre_load, post_dump, pre_dump, INCLUDE
from iroko.taxonomy.api import Terms
from iroko.taxonomy.marshmallow import term_schema

from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import SanitizedUnicode


class IdentifierSchema(StrictKeysMixin):
    """Ids schema."""

    idtype = SanitizedUnicode()
    value = SanitizedUnicode()


class TermSourcesSchema(Schema):
    term_id = fields.Int()
    sources_id = fields.Int()
    data = fields.Raw(many=False)

    @post_dump
    def dump_term(self, termSource, **kwargs):
        # TODO: version_to_review is true cuando tiene una version con una fecha posterior a la version current.
        # print("################################")
        # print(termSource)
        # if termSource and 'term_id' in termSource:
        msg, term = Terms.get_term_by_id(termSource['term_id'])
        termSource['term'] = term_schema.dump(term)

        return termSource


class SourceDataSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    term_sources = fields.List(fields.Nested(TermSourcesSchema))
    source_uuid = fields.UUID(dump_only=True)
    identifiers = fields.Nested(IdentifierSchema, many=True)


# TODO: to replace by UserProfilesSchema
class IrokoUserSchema(Schema):
    email = fields.Str()


source_data_schema = SourceDataSchema(many=False, unknown=INCLUDE)
