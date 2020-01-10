from typing import Dict

from invenio_db import db
from flask_login import current_user
from iroko.taxonomy.models import Vocabulary, Term, TermClasification
from iroko.sources.models import TermSources
from iroko.taxonomy.marshmallow import vocabulary_schema_many, vocabulary_schema, term_schema_many, term_schema
from flask_babelex import lazy_gettext as _
from marshmallow import ValidationError
from iroko.taxonomy.permissions import grant_vocabulary_editor_permission

class Vocabularies:
    '''Manage vocabularies'''

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
            valid_data, errors = vocabulary_schema.load(data)
            if not errors:
                vocab.human_name = valid_data['human_name']
                vocab.description = valid_data['description']
                vocab.data = valid_data['data']
                db.session.commit()
                msg = 'New Vocabulary UPDATED name={0}'.format(vocab.name)
            else:
                msg = errors
                vocab = None
        return msg, vocab


    @classmethod
    def new_vocabulary(cls, data) -> Dict[str, Vocabulary]:

        valid_data, errors = vocabulary_schema.load(data)
        if not errors:
            vocab = Vocabulary.query.filter_by(name=valid_data['name']).first()
            if not vocab:
                vocab = Vocabulary()
                vocab.name = valid_data['name']
                vocab.human_name = valid_data['human_name']
                vocab.description = valid_data['description']
                vocab.data = valid_data['data']
                db.session.add(vocab)
                db.session.commit()

                if current_user:
                   yesss = grant_vocabulary_editor_permission(current_user, vocab)
                   print(yesss)

                msg = 'New Vocabulary CREATED name={0}'.format(vocab.name)
            else:
                msg = 'Vocabulary already exist name={0}'.format(vocab.name)
                vocab = None
        else:
            msg = errors
            vocab = None
        return msg, vocab


class Terms:
    """Manage Terms"""


    @classmethod
    def get_term(cls, uuid) -> Dict[str, Term]:
        term = Term.query.filter_by(uuid=uuid).first()
        if term:
            return 'ok', term
        else:
            msg = 'Term not exist uuid={0}'.format(uuid)
            return msg, None

    @classmethod
    def edit_term(cls, uuid ,data) -> Dict[str, Term]:

        msg, term = cls.get_term(uuid)
        if term:
            valid_data, errors = term_schema.load(data)
            if not errors:
                cls._update_term_data(term, valid_data)
                db.session.commit()
                cls._update_term_clasification(term, valid_data)
                db.session.commit()
                msg = 'New Term UPDATED name={0}'.format(term.name)
            else:
                msg = str(errors)
                term = None
        return msg, term


    @classmethod
    def new_term(cls, data) -> Dict[str, Term]:

        valid_data, errors = term_schema.load(data)
        if not errors:
            term = Term.query.filter_by(name=valid_data['name']).first()
            if not term:
                term = Term()
                cls._update_term_data(term, valid_data)
                db.session.add(term)
                db.session.commit()
                cls._update_term_clasification(term, valid_data)
                db.session.commit()
                msg = 'New Term CREATED id={0}'.format(term.id)
            else:
                msg = 'Term already exist name={0}'.format(valid_data['name'])
                term = None
        else:
            msg = str(data) + str(valid_data)
            term = None
        return msg, term



    @classmethod
    def _update_term_data(cls, term: Term, data):
        ''''''

        term.vocabulary_id = data['vocabulary_id']
        term.name = data['name']
        term.description = data['description']
        term.parent_id = data['parent_id']
        term.data = data['data']

    @classmethod
    def _update_term_clasification(cls, term: Term, data):
        '''
        this search all clasification of the term, delete it, and then create new clasification based on params

        # TODO: This will be replaced by the graph database, when done....

        in data:
        class_ids: IDs of Terms that clasifies this term
        clasified_ids: IDs of Terms clasified by this term
        '''

        # delete all Clasifications in wich this term is envolved
        TermClasification.query.filter_by(term_class_id=term.id).delete()
        TermClasification.query.filter_by(term_clasified_id=term.id).delete()
        db.session.commit()

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
            lista = Term.query.filter(Vocabulary.name==vocabulary_name).order_by('name').all()            
            print(lista[0].id)
            return lista
        except Exception as error:
            return []
        