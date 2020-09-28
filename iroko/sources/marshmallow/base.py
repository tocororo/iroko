

from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import SanitizedUnicode, PersistentIdentifier
from marshmallow import Schema, fields, post_dump, INCLUDE

from iroko.vocabularies.api import Terms
from iroko.vocabularies.marshmallow import term_schema


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


class ClasificationDataSchema(Schema):
    id = fields.UUID()
    description = fields.Str()
    vocabulary = fields.Str()
    data = fields.Raw(many=False)


class OrganizationDataSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    role = fields.Str()


class SavingInfoSchema(Schema):
    user_id = fields.Str()
    comment = fields.Str()


class SourceDataSchema(Schema):
    id = PersistentIdentifier()
    identifiers = fields.Nested(IdentifierSchema, many=True)
    name = fields.Str(allow_none=False)
    source_type = fields.Str(allow_none=False)
    source_status = fields.Str(allow_none=True)
    title = fields.Str()
    description = fields.Str()

    organizations = fields.Nested(OrganizationDataSchema, many=True, unknown=INCLUDE)
    classifications = fields.Nested(ClasificationDataSchema, many=True, unknown=INCLUDE)

    _save_info = fields.Nested(SavingInfoSchema, many=False, unknown=INCLUDE)


# TODO: to replace by UserProfilesSchema
class IrokoUserSchema(Schema):
    email = fields.Str()


source_data_schema = SourceDataSchema(many=False, unknown=INCLUDE)
