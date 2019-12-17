
from marshmallow import Schema, fields

from iroko.sources.marshmallow import BaseSourceSchema

class ISSNSchema(Schema):
    p = fields.Str()
    e = fields.Str()
    l = fields.Str()

class JournalDataSchema(Schema):
    """JournalDataSchema specific data for academic journals """

    title = fields.Str()
    description = fields.Str()
    url = fields.Url()
    issn = fields.Nested(ISSNSchema, many=False)
    rnps = fields.Str()
    email = fields.Str()
    logo = fields.Str()
    seriadas_cubanas = fields.Url()
    year_start = fields.DateTime()
    year_end = fields.DateTime()

class JournalSchema(BaseSourceSchema):
    data = fields.Nested(JournalDataSchema, many=False)

journal_schema = JournalSchema()
journal_schema_many = JournalSchema(many=True)
