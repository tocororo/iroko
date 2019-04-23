
from marshmallow import Schema, fields



class HarvestingDataSchema(Schema):

    metadata_schema = fields.Str()
    validation = fields.Str()
    information = fields.List(fields.Str())


class HarvestedItemSchema(Schema):
    id = fields.Int()
    source_id = fields.Int()
    identifier = fields.Str()
    record = fields.UUID()

    status = fields.Str()
    harvesting_data = fields.Nested(HarvestingDataSchema, many=True)



# sources_schema = SourcesSchema(many=True, only=('id', 'uuid', 'name', 'source_type'))
# sources_schema_full = SourcesSchema(many=True)
# term_source_schema = TermSourcesSchema()