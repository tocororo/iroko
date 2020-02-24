from typing import Dict

from invenio_db import db
from sqlalchemy import exc as sqlalchemyExc
from invenio_access.utils import get_identity
from flask_login import current_user
from iroko.taxonomy.models import Vocabulary, Term, TermClasification
from iroko.sources.models import TermSources
from iroko.taxonomy.marshmallow import vocabulary_schema_many, vocabulary_schema, term_schema_many, term_schema, term_node_schema, term_node_schema_many, term_schema_no_clases
from flask_babelex import lazy_gettext as _
from marshmallow import ValidationError
from invenio_access import Permission
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from iroko.taxonomy.permissions import ObjectVocabularyEditor, is_current_user_taxonomy_admin



#TODO: Revisar lanzamientos de excepciones

class Vocabularies:
    '''Manage vocabularies'''

    @classmethod
    def get_vocabularies(cls):
        return Vocabulary.query.all()

    @classmethod
    def get_vocabulary(cls, id) -> Dict[str, Vocabulary]:

        vocab = Vocabulary.query.filter_by(id=id).first()
        if vocab:
            return 'ok', vocab
        else:
            msg = 'Vocabulary not exist id={0}'.format(id)
            return msg, None


    @classmethod
    def edit_vocabulary(cls, id ,data) -> Dict[str, Vocabulary]:

        msg, vocab = cls.get_vocabulary(id)
        if vocab:
            try:
                valid_data = vocabulary_schema.load(data)
                vocab.human_name = valid_data['human_name']
                vocab.description = valid_data['description']
                vocab.data = valid_data['data']
                db.session.commit()
                msg = 'New Vocabulary UPDATED name={0}'.format(vocab.name)
            except Exception as err:
                msg = 'ERROR {0} - {1}'.format(err, data)
            finally:
                return msg, vocab
        else:
            return msg, vocab

    @classmethod
    def new_vocabulary(cls, input_data) -> Dict[str, Vocabulary]:

        msg = ''
        try:
            data = vocabulary_schema.load(input_data)
            vocab = Vocabulary.query.filter_by(name=data['name']).first()
            if not vocab:
                vocab = Vocabulary()
                vocab.name = data['name']
                vocab.human_name = data['human_name']
                vocab.description = data['description']
                vocab.data = data['data']
                db.session.add(vocab)
                db.session.commit()
                msg = 'New Vocabulary CREATED name={0}'.format(vocab.name)
            else:
                msg = 'Vocabulary already exist name={0}'.format(vocab.name)
                vocab = None
        except Exception as err:
            msg = 'ERROR {0} - {1}'.format(err, data)
            vocab = None
        finally:
            return msg, vocab


    @classmethod
    def grant_vocabulary_editor_permission(cls, user_id, vocabulary_id) -> Dict[str, bool]:
        done = False
        msg = ''
        try:
            vocabulary = Vocabulary.query.filter_by(id=vocabulary_id).first()
            user = User.query.filter_by(id=user_id).first()
            if not vocabulary:
                msg = 'Vocabulary not found'
            elif not user:
                msg = 'User not found'
            else:
                db.session.add(ActionUsers.allow(ObjectVocabularyEditor(vocabulary.id), user=user))
                db.session.commit()
                msg = 'Vocabulary Editor Permission granted over {0}'.format(vocabulary.name)
                done = True

        except Exception as e:
            msg = str(e)
            print(str(e))

        return msg, done

    @classmethod
    def deny_vocabulary_editor_permission(user_id, vocabulary_id) -> Dict[str, bool]:
        done = False
        msg = ''
        try:
            vocabulary = Vocabulary.query.filter_by(id=vocabulary_id).first()
            user = User.query.filter_by(id=user_id).first()
            if not vocabulary:
                msg = 'Vocabulary not found'
            elif not user:
                msg = 'User not found'
            else:
                db.session.add(ActionUsers.deny(ObjectVocabularyEditor(vocabulary.id), user=user))
                db.session.commit()
                msg = 'Editor Permission granted over {0}'.format(vocabulary.name)
                done = True

        except Exception as e:
            print(str(e))

        return msg, done

    @classmethod
    def check_user_vocabulary_editor_permission(user_id, vocabulary_id)-> Dict[str, bool]:
        done = False
        msg = ''
        try:
            if is_current_user_taxonomy_admin():
                done= True
            else:
                vocabulary = Vocabulary.query.filter_by(id=vocabulary_id).first()
                user = User.query.filter_by(id=user_id)
                user_identity = get_identity(user)
                permission = Permission(ObjectVocabularyEditor(vocabulary.id))
                done = permission.allows(user_identity)
        except Exception as e:
            msg = str(e)
            print(str(e))

        return msg, done

class Terms:
    """Manage Terms"""

    @classmethod
    def get_terms(cls):
        return Term.query.all()

    @classmethod
    def get_terms_by_vocab(cls, vocabulary_id) -> Dict[str, Term]:
        msg, vocab = Vocabularies.get_vocabulary(vocabulary_id)
        if not vocab:
            raise Exception(msg)
        terms = vocab.terms

        return 'ok', terms

    @classmethod
    def get_first_level_terms_by_vocabulary(cls, vocabulary_id)-> Dict[str, Term]:

        msg, vocab = Vocabularies.get_vocabulary(vocabulary_id)
        if not vocab:
            raise Exception(msg)
        terms = vocab.terms.filter_by(parent_id=None).all()

        return 'ok', vocab, terms


    # @classmethod
    # def get_terms_tree_by_vocabulary(cls, vocabulary_id, level: int)-> [str, Vocabulary, list]:
    #     """If level < 0, means all the levels of the tree"""
    #     msg, vocab = Vocabularies.get_vocabulary(vocabulary_id)
    #     if not vocab:
    #         raise Exception(msg)

    #     msg, terms = Terms.get_first_level_terms_by_vocabulary(vocabulary_id)

    #     terms_full = []
    #     for term in terms:
    #         terms_full.append(term_node_schema.dump_term_node(term, level, 0))

    #     return 'ok', vocab, terms_full

    @classmethod
    def get_term(cls, uuid) -> Dict[str, Term]:
        term = Term.query.filter_by(uuid=uuid).first()
        if term:
            return 'ok', term
        else:
            msg = 'Term not exist uuid={0}'.format(uuid)
            return msg, None

    @classmethod
    def get_terms_by_uuid_list(cls, uuid_list) :
        terms = Term.query.filter(Term.uuid.in_(uuid_list)).all()
        return terms

    @classmethod
    def get_term_by_id(cls, id) -> Dict[str, Term]:
        term = Term.query.filter_by(id=id).first()
        if term:
            return 'ok', term
        else:
            msg = 'Term not exist id={0}'.format(id)
            return msg, None

    @classmethod
    def edit_term(cls, uuid, input_data) -> Dict[str, Term]:
        msg = ''
        try:
            data = term_schema.load(input_data)
            term = Term.query.filter_by(uuid=uuid).first()
            term.vocabulary_id = data['vocabulary_id']
            term.name = data['name']
            term.description = data['description']
            term.parent_id = data['parent_id']
            term.data = data['data']
            # cls._update_term_data(term, data)
            print(term.data)
            try:
                db.session.commit()
                cls._update_term_clasification(term, data)
                msg = 'New Term UPDATED name={0}'.format(term.name)
                return msg, term
            except sqlalchemyExc.SQLAlchemyError as e:
                msg = 'sqlalthemy: {0}'.format(e)
                db.session.rollback()
                return msg, None

        except Exception as e:
            msg = 'ERROR {0} - {1}'.format(e, input_data)
            return msg, None


    @classmethod
    def new_term(cls, data) -> Dict[str, Term]:
        msg = ''
        # try:
        valid_data = term_schema.load(data)

        term = Term.query.filter_by(name=valid_data['name']).first()
        if not term:
            print(valid_data)
            term = Term()
            term.vocabulary_id = valid_data['vocabulary_id']
            term.name = valid_data['name']
            term.description = valid_data['description']
            term.parent_id = valid_data['parent_id']
            term.data = valid_data['data']
            print(term.data)
            db.session.add(term)
            print(term)
            try:
                db.session.commit()
                cls._update_term_clasification(term, valid_data)
                msg = 'New Term CREATED name={0}'.format(term.name)
                return msg, term
            except sqlalchemyExc.SQLAlchemyError as e:
                msg = 'sqlalthemy: {0}'.format(e)
                db.session.rollback()
                return msg, None
        else:
            msg = 'Term already exist name={0}'.format(valid_data['name'])
            return msg, None
        # except Exception as e:
        #     msg = 'ERROR {0} - {1}'.format(e, data)
        #     return msg, None


    # @classmethod
    # def _get_term_data(cls, term: Term, data):
    #     ''''''
    #     # return {
    #     #     'vocabulary_id': data['vocabulary_id'],
    #     #     'name': data['name'],
    #     #     'description': data['description'],
    #     #     'parent_id': data['parent_id'],
    #     #     'data': data['data'],
    #     # }

    #     print(data)
    #     term.vocabulary_id = data['vocabulary_id']
    #     print(data)
    #     term.name = data['name']
    #     print(data)
    #     term.description = data['description']
    #     print(data)
    #     term.parent_id = data['parent_id']
    #     print(data)
    #     term.data = data['data']
    #     print(data)


    @classmethod
    def _update_term_data(cls, term: Term, data):
        ''''''
        # return {
        #     'vocabulary_id': data['vocabulary_id'],
        #     'name': data['name'],
        #     'description': data['description'],
        #     'parent_id': data['parent_id'],
        #     'data': data['data'],
        # }

        print(data)
        term.vocabulary_id = data['vocabulary_id']
        print(data)
        term.name = data['name']
        print(data)
        term.description = data['description']
        print(data)
        term.parent_id = data['parent_id']
        print(data)
        term.data = data['data']
        print(data)


    @classmethod
    def _update_term_clasification(cls, term: Term, data):
        '''
        this search all clasification of the term, delete it, and then create new clasification based on params

        # TODO: This will be replaced by the graph database, when done....

        in data:
        class_ids: IDs of Terms that clasifies this term
        clasified_ids: IDs of Terms clasified by this term
        '''
        print('_update_term_clasification', data)
        # delete all Clasifications in wich this term is envolved
        TermClasification.query.filter_by(term_class_id=term.id).delete()
        TermClasification.query.filter_by(term_clasified_id=term.id).delete()
        db.session.commit()
        print('_update_term_clasification', data)
        # Terms clasified by this term
        for clasified_ids in data['clasified_ids']:
            clasified = Term.query.filter_by(id=clasified_ids).first()
            if clasified:
                clasification = TermClasification()
                clasification.term_class_id = term.id
                clasification.term_clasified_id = clasified.id
                db.session.add(clasification)

        # Terms that clasifies this term
        for class_id in data['class_ids']:
            t_class = Term.query.filter_by(id=class_id).first()
            if t_class:
                clasification = TermClasification()
                clasification.term_class_id = t_class.id
                clasification.term_clasified_id = term.id
                db.session.add(clasification)
        db.session.commit()
        print('_update_term_clasification', data)


    @classmethod
    def delete_term(cls, uuid) -> Dict[str, bool]:
        try:
            term = Term.query.filter_by(uuid=uuid).first()
            if term:
                if len(term.children) > 0:
                    return _('No se puede eliminar el término cuando otros términos dependen de él'), False

                in_clasification = TermClasification.query.filter_by(term_class_id=term.id).first()
                if in_clasification:
                    return _('No se puede eliminar el término si clasificaciones dependen de él'), False

                in_source = TermSources.query.filter_by(term_id=term.id).first()
                if in_source:
                    return _('No se puede eliminar el término si fuentes dependen de él'), False

                db.session.query(TermClasification).filter_by(term_object_id=term.id).delete()
                db.session.delete(term)
                db.session.commit()
                return 'Término: {0}, eliminado satisfactoriamente'.format(term.name), True

        except Exception as e:
            return str(e), False

    @classmethod
    def get_terms_by_vocabulary_name(cls, vocabulary_name):
        try:
            lista = Term.query.join(Term.vocabulary, aliased=True).filter_by(name=vocabulary_name)
            print(lista[0].id)
            return lista
        except Exception as error:
            return []

    # @classmethod
    # def dump_term(cls, term:Term, level_to_reach: int, current_level: int):
    #     """ helper function to load terms children"""
    #     if current_level < level_to_reach:
    #         children = []
    #         for child in term.children:
    #             children.append(Terms.dump_term(child, level_to_reach, current_level+1))
    #         return {'term': term_schema.dump(term), 'children':children}
    #     else:
    #         return term_schema.dump(term)



def get_current_user_permissions() -> Dict[str, Dict[str, list]]:
    """
    Checks from ActionUsers if current_user has taxonomy_full_editor_actions,
    that way it has full permissions over vocabularies and terms
    if not, then:
        checks if it has vocabulary_editor_actions,
        then collect the ids of the vocabularies it has permission on
    """
    vocabularies_ids = []
    if is_current_user_taxonomy_admin():
        return 'actions', {'taxonomy_full_editor_actions': None}
    else:
        actions = ActionUsers.query.filter_by(
            user=current_user,
            exclude=False,
            action='vocabulary_editor_actions').all()

        for action in actions:
            vocabularies_ids.append(action.argument)

    return 'actions', {'vocabulary_editor_actions': vocabularies_ids}

