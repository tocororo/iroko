
from marshmallow import Schema, fields, ValidationError, pre_load
from iroko.taxonomy.models import Vocabulary, Term



class TermSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    parent_id = fields.Int()
    # vocabulary = fields.Nested()
    # children = fields.Nested('TermSchema')

class VocabularySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    # terms = fields.Nested(TermSchema)

terms_schema = TermSchema(many=True, only=('id', 'uuid', 'name'))
term_schema = TermSchema()
vocabularies_schema = VocabularySchema(many=True, only=('id', 'name', 'description'))
vocabulary_schema = VocabularySchema()