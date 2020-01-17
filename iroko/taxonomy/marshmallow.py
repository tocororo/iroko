
from marshmallow import Schema, fields, ValidationError, pre_load, pre_dump, post_load, post_dump
from iroko.taxonomy.models import Vocabulary, Term, TermClasification


class VocabularySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    human_name = fields.Str(required=True)
    description = fields.Str(allow_none=True)

    # in case to put anything in the future
    data = fields.Raw(allow_none=True)

    @post_load
    def vocabulary_load(self, item, **kwargs):
        # TODO: Add here fix to the name (no spaces, not capitals... etc...)
        item['description'] = item['description'] if 'description' in item else ''
        item['data'] = item['data'] if 'data' in item else {}
        return item


class TermSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    parent_id = fields.Int(allow_none=True)

    # this field depend on the vocabulary of the term, can be anything
    data = fields.Raw(allow_none=True)

    vocabulary_id = fields.Int(required=True)

    # ids of terms clasified by this term
    class_ids = fields.List(fields.Int())
    # ids of terms that clasifies this term
    clasified_ids = fields.List(fields.Int())

    @pre_load
    def load_clasification(self, item, **kwargs):
        item['description'] = item['description'] if 'description' in item else ''
        item['class_ids'] = item['class_ids'] if 'class_ids' in item else []
        item['clasified_ids'] = item['clasified_ids'] if 'clasified_ids' in item else []
        item['data'] = item['data'] if 'data' in item else {}
        item['parent_id'] = item['parent_id'] if 'parent_id' in item else None
        return item

    @pre_dump
    def dump_clasification(self, term, **kwargs):
        term.class_ids = []
        for term_class in TermClasification.query.filter_by(term_clasified_id=term.id).all():
            term.class_ids.append(term_class.term_class_id)

        term.clasified_ids = []
        for term_clasification in TermClasification.query.filter_by(term_class_id=term.id).all():
            term.clasified_ids.append(term_clasification.term_clasified_id)

        return term



# unknown='EXCLUDE', esto se pone para que el load excluya los campos que no se conoce, 
# lo estamos usando aqui porque los campos dump_only se interpretan por marshmallow 3 como desconocidos
# si no se pone unknown='EXCLUDE' entonces en los PUT (que hace load) no pueden venir los dump_only
# basicamente los dump_only nuestros son id y uuid
# https://stackoverflow.com/questions/54391524/sqlalchemy-property-causes-unknown-field-error-in-marshmallow-with-dump-only/54405610#54405610
# https://github.com/marshmallow-code/marshmallow/issues/875

# al final el cliente, debe manejar el problema de excluir los campos id y uuid del input en un PUT



term_schema_many = TermSchema(many=True, only=('id', 'uuid', 'name'))
term_schema = TermSchema(many=False)
vocabulary_schema_many = VocabularySchema(many=True, only=('id', 'name', 'human_name', 'description'))
vocabulary_schema = VocabularySchema(many=False)
