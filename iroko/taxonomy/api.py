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
            # data = vocabulary_schema.loads(input_data)
            vocab.name = data['name']
            vocab.description = data['description']
            if 'data' in data: 
                vocab.data = data['data']
            db.session.commit()
            msg = 'New Vocabulary UPDATED id={0}'.format(vocab.id)
        return msg, vocab

    @classmethod
    def new_vocabulary(cls, data) -> Dict[str, Vocabulary]:

        # data = vocabulary_schema.loads(input_data)
        vocab = Vocabulary.query.filter_by(name=data['name']).first()
        if not vocab:
            vocab = Vocabulary()
            vocab.name = data['name']
            vocab.description = data['description']
            if 'data' in data: 
                vocab.data = data['data']
            db.session.add(vocab)
            db.session.commit()
            msg = 'New Vocabulary CREATED id={0}'.format(vocab.id)
            return msg, vocab
        else:
            msg = 'Vocabulary already exist name={0}'.format(data['name'])
            return msg, None



class Terms:
    """Manage Terms"""

    @classmethod
    def get_term(id):
        print('not implemented yet')

    @classmethod
    def new_term(cls, input_data):
        print('not implemented yet')