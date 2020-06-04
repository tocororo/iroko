from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import PersistentIdentifier
from marshmallow import Schema, fields

from iroko.records.marshmallow.json import IdentifierSchemaV1
from iroko.sources.marshmallow.journal import JournalDataSchema


class OrganizationLabelSchema(Schema):
    label = fields.Str(allow_none=False)
    iso639 = fields.Str(allow_none=False)


class OrganizationRelationshipSchema(Schema):
    identifiers = fields.Nested(IdentifierSchemaV1, many=True)
    type = fields.Str(allow_none=False)
    label = fields.Str(allow_none=False)


class OrganizationDataSchemaV1(JournalDataSchema):

    identifiers = fields.Nested(IdentifierSchemaV1, many=True)
    name = fields.Str(allow_none=False)
    status = fields.Str(allow_none=False)
    aliases = fields.List(fields.Str)
    acronyms = fields.List(fields.Str)
    types = fields.List(fields.Str)
    wikipedia_url = fields.URL()
    email_address = fields.Email()
    ip_addresses = fields.Str()
    established = fields.Integer()
    links = fields.List(fields.URL)
    labels = fields.List(fields.Nested(OrganizationLabelSchema))
    relationships = fields.List(fields.Nested(OrganizationRelationshipSchema))


class OrganizationSchemaV1(StrictKeysMixin):
    """Source schema."""

    metadata = fields.Nested(OrganizationDataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()

