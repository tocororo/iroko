

from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import DateString, SanitizedUnicode, PersistentIdentifier
from marshmallow import Schema, fields, post_dump, INCLUDE

from iroko.userprofiles import UserProfile
from iroko.userprofiles.marshmallow import UserProfilesSchema, userprofile_schema
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



class RelationSchemaV1(Schema):
    """Ids schema."""

    identifiers = fields.Nested(IdentifierSchema, many=True, required=True)
    type = SanitizedUnicode()
    label = SanitizedUnicode()


class OrganizationDataSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    role = fields.Str()
    status = SanitizedUnicode()
    identifiers = fields.Nested(IdentifierSchema, many=True)
    relationships = fields.Nested(RelationSchemaV1, many=True)


class SavingInfoSchema(Schema):
    user_id = fields.Str()
    comment = fields.Str()
    updated = DateString()


class SourceDataSchema(Schema):
    id = PersistentIdentifier()
    identifiers = fields.Nested(IdentifierSchema, many=True)
    name = fields.Str(allow_none=False)
    source_type = fields.Str(allow_none=False)
    source_status = fields.Str(allow_none=True)
    source_system = fields.Str()
    title = fields.Str()
    description = fields.Str()

    organizations = fields.Nested(OrganizationDataSchema, many=True, unknown=INCLUDE)
    classifications = fields.Nested(ClasificationDataSchema, many=True, unknown=INCLUDE)

    _save_info = fields.Nested(SavingInfoSchema, many=False, unknown=INCLUDE)
    _save_info_updated = DateString()


class IrokoUserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    profile = fields.Nested(UserProfilesSchema, many=False)

    @post_dump
    def dump_profile(self, user, **kwargs):
        profile = UserProfile.get_or_create_by_userid(user['id'])
        user['profile'] = userprofile_schema.dump(profile)
        return user





source_base_data_schema = SourceDataSchema(many=False, unknown=INCLUDE)
