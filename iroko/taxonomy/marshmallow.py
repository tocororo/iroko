
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

    # parent = fields.Nested(TermSchema, many=False, dump_only=True)
    # children = fields.Nested(TermSchema, many=True, dump_only=True)

    # def __init__(self, *args, **kwargs):
    #     self.level_to_reach = kwargs.pop('level_to_reach') if 'level_to_reach' in kwargs else 0
    #     super(Schema, self).__init__(*args, **kwargs)


    @pre_load
    def load_clasification(self, item, **kwargs):
        item['description'] = item['description'] if 'description' in item else ''
        item['class_ids'] = item['class_ids'] if 'class_ids' in item else []
        item['clasified_ids'] = item['clasified_ids'] if 'clasified_ids' in item else []
        item['data'] = item['data'] if 'data' in item else {}
        item['parent_id'] = item['parent_id'] if 'parent_id' in item else None
        return item

    @pre_dump
    def dump_clasification(self, term: Term, **kwargs):
        if not term is None:
            term.class_ids = []
            for term_class in TermClasification.query.filter_by(term_clasified_id=term.id).all():
                term.class_ids.append(term_class.term_class_id)

            term.clasified_ids = []
            for term_clasification in TermClasification.query.filter_by(term_class_id=term.id).all():
                term.clasified_ids.append(term_clasification.term_clasified_id)

        return term

    # @post_dump
    # def dump_term_node(self, term:Term):
    #     if level_to_reach < 0 :
    #         if term.parent_id is None or level_to_reach == current_level:
    #             return term_schema.dump(term)
    #         if level_to_reach < current_level:
    #             parent = Term.query.filter_by(id=term.parent_id).first()
    #             return {
    #                 'term': term_schema.dump(term),
    #                 'parent': self.dump_term_node(parent, level_to_reach, current_level - 1)
    #             }
    #     elif level_to_reach > 0 :
    #         if current_level < level_to_reach:
    #             children = []
    #             for child in term.children:
    #                 children.append(self.dump_term_node(child, level_to_reach, current_level + 1))
    #             return {
    #                 'term': term_schema.dump(term),
    #                 'children':children
    #                 }
    #     else:
    #         return {'term': term_schema.dump(term)}

    # def get_term_hierarchy(self, term, current_level):
    #     if self.level_to_reach < 0:
    #         if self.level_to_reach < current_level:
    #             return TermSchema(self)

class TermNodeSchema(Schema):
    """I'm not sure that this is the way marshmallow should be used, but this is a better place to put the tree recursive function dump_term.
    At the end, this is an special dump, probably the way to go is redefining somehow the dump function of marshmallow, but y think this is not pre_dump or post_dump problem.
    Any way, this Schema should be used calling dump_term_node, not dump.

    TODO: Creo que esto deberia ponerse en TermSchema,
    y aunque logicamente afectaria los clientes, me parece mas consistente lograr eso mismo usando el dump propio de marshmallow,
    lo que habria que buscar como pasar los argumentos  level_to_reach y current_level

     """



    term = fields.Nested(TermSchema, many=False)
    parent = fields.Nested(TermSchema, many=False)
    children = fields.Nested(TermSchema, many=True)

    def dump_term_node(self, term:Term, level_to_reach: int, current_level: int):
        if level_to_reach < 0 :
            if term.parent_id is None or level_to_reach == current_level:
                return {
                    'term': term_schema.dump(term),
                    'parent': None
                }
            if level_to_reach < current_level:
                parent = Term.query.filter_by(id=term.parent_id).first()
                return {
                    'term': term_schema.dump(term),
                    'parent': self.dump_term_node(parent, level_to_reach, current_level - 1)
                }
        elif level_to_reach > 0 :
            if current_level < level_to_reach:
                children = []
                for child in term.children:
                    children.append(self.dump_term_node(child, level_to_reach, current_level + 1))
                return {
                    'term': term_schema.dump(term),
                    'children':children
                    }
            else:
                return {
                    'term': term_schema.dump(term),
                    'children': None
                    }
        else:
            return {'term': term_schema.dump(term)}

    def dump_term_node_list(self, terms, level_to_reach: int, current_level: int):
        result = []
        for term in terms:
            result.append(self.dump_term_node(term, level_to_reach, current_level))
        return result



# unknown='EXCLUDE', esto se pone para que el load excluya los campos que no se conoce,
# lo estamos usando aqui porque los campos dump_only se interpretan por marshmallow 3 como desconocidos
# si no se pone unknown='EXCLUDE' entonces en los PUT (que hace load) no pueden venir los dump_only
# basicamente los dump_only nuestros son id y uuid
# https://stackoverflow.com/questions/54391524/sqlalchemy-property-causes-unknown-field-error-in-marshmallow-with-dump-only/54405610#54405610
# https://github.com/marshmallow-code/marshmallow/issues/875

# al final el cliente, debe manejar el problema de excluir los campos id y uuid del input en un PUT

term_node_schema_many = TermNodeSchema(many=True)
term_node_schema = TermNodeSchema(many=False)

term_schema_many = TermSchema(many=True, only=('id', 'uuid', 'name'))
term_schema = TermSchema(many=False)
vocabulary_schema_many = VocabularySchema(many=True, only=('id', 'name', 'human_name', 'description'))
vocabulary_schema = VocabularySchema(many=False)
