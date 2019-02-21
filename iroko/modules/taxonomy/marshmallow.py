
from marshmallow import Schema, fields, ValidationError, pre_load
from iroko.modules.taxonomy.models import Vocabulary, Term



class TermSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    # vocabulary = fields.Nested()
    children = fields.Nested('TermSchema')

class VocabularySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    # terms = fields.Nested(TermSchema)

terms_schema = TermSchema(many=True, only=('id', 'name', 'uuid', 'description'))
vocabularies_schema = VocabularySchema(many=True, only=('id', 'name', 'description'))
vocabulary_schema = VocabularySchema()