from marshmallow import Schema, fields, validate

class RuleSchema(Schema):
    key = fields.Str(required=True)
    value = fields.List(fields.Str(), required=True)

class RelationshipSchema(Schema):
    type = fields.Str(required=True)
    relation = fields.Str(required=True)
    description = fields.Str()
    identifier = fields.Str()

class NestedMappingsSchema(Schema):
    nested_mappings = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str()))

class MappingSchema(Schema):
    _class = fields.Str(required=True)
    required = fields.List(fields.Str(), required=True)
    properties = fields.Dict(keys=fields.Str(), values=fields.Nested(NestedMappingsSchema) | fields.Str() | fields.List(fields.Str()))
    valuesOf = fields.Dict(keys=fields.Str(), values=fields.Dict(keys=fields.Str(), values=fields.Str()))

class EntitySchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    mapping = fields.Nested(MappingSchema, required=True)

class ConfigurationSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    created = fields.Str(required=True)
    last_updated = fields.Str(required=True)
    order_for_mapping = fields.List(fields.Str(), required=True)
    entities = fields.List(fields.Nested(EntitySchema), required=True)

 