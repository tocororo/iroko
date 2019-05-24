
from marshmallow import Schema, fields
from iroko.harvester.models import HarvestedItem


class HarvestedItemSchema(Schema):
    id = fields.Int(dump_only=True)
    repository_id = fields.Int()
    identifier = fields.Str()
    record = fields.Str()
    status = fields.Str()
    error_log = fields.Str()

items_schema = HarvestedItemSchema(many=True)