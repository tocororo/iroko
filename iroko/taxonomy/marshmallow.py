
from marshmallow import Schema, fields, ValidationError, pre_load
from iroko.taxonomy.models import Vocabulary, Term


class VocabularySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    
    # in case to put anything in the future
    data = fields.Raw()


class TermSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    parent_id = fields.Int()
    
    # this field depend on the vocabulary of the term, can be anything
    data = fields.Raw()
    vocabulary = fields.Nested(VocabularySchema, many=False)


term_schema_many = TermSchema(many=True, only=('id', 'uuid', 'name'))
term_schema = TermSchema()
vocabulary_schema_many = VocabularySchema(many=True, only=('id', 'name', 'description'))
vocabulary_schema = VocabularySchema()