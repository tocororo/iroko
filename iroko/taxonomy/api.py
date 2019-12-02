from typing import Dict

from invenio_db import db

from iroko.taxonomy.models import Vocabulary, Term
from iroko.taxonomy.marshmallow import vocabulary_schema_many, vocabulary_schema, term_schema_many, term_schema


class Vocabularies:
    """Manage vocabularies"""

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
            vocab.name = data['name']
            vocab.description = data['description']
            if 'data' in data:
                vocab.data = data['data']
            db.session.commit()
            msg = 'New Vocabulary UPDATED name={0}'.format(vocab.name)
        return msg, vocab

    @classmethod
    def new_vocabulary(cls, data) -> Dict[str, Vocabulary]:

        vocab = Vocabulary.query.filter_by(name=data['name']).first()
        if not vocab:
            vocab = Vocabulary()
            vocab.name = data['name']
            vocab.description = data['description']
            if 'data' in data:
                vocab.data = data['data']
            db.session.add(vocab)
            db.session.commit()
            msg = 'New Vocabulary CREATED name={0}'.format(vocab.name)
            return msg, vocab
        else:
            msg = 'Vocabulary already exist name={0}'.format(data['name'])
            return msg, None



class Terms:
    """Manage Terms"""


    @classmethod
    def get_term(cls, id) -> Dict[str, Term]:
        term = Term.query.filter_by(uuid=id).first()
        if term:
            return 'ok', term
        else:
            msg = 'Term not exist id={0}'.format(id)
            return msg, None

    @classmethod
    def edit_term(cls, id ,data) -> Dict[str, Term]:

        msg, term = cls.get_term(id)
        if term:
            term.name = data['name']
            term.description = data['description']
            if 'data' in data:
                term.data = data['data']
            db.session.commit()
            msg = 'New Term UPDATED name={0}'.format(term.name)
        return msg, term

    @classmethod
    def new_term(cls, data) -> Dict[str, Term]:

        term = Term.query.filter_by(name=data['name']).first()
        if not term:
            term = Term()
            term.name = data['name']
            term.description = data['description']
            if 'data' in data:
                term.data = data['data']
            db.session.add(term)
            db.session.commit()
            msg = 'New Term CREATED id={0}'.format(term.id)
            return msg, term
        else:
            msg = 'Term already exist name={0}'.format(data['name'])
            return msg, None
