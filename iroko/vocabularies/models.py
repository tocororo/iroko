

"""Iroko Taxonomy Admin models."""

import uuid

from invenio_db import db
from sqlalchemy_utils.types import UUIDType, JSONType


class Vocabulary(db.Model):
    """Define a Vocabulary"""

    __tablename__ = 'iroko_vocab'

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String, nullable=False, unique=True)
    human_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)

    # any data related to the vocabulary
    data = db.Column( JSONType )


    def __str__(self):
        """Representation."""
        return self.identifier


class Term(db.Model):
    __tablename__ = 'iroko_terms'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType, default=uuid.uuid4)
    # TODO: reemplazar name por identifier y ponerlo unico.
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    vocabulary_id = db.Column(db.String(),
                        db.ForeignKey('iroko_vocab.identifier', ondelete='CASCADE'),
                        nullable=False, index=True)
    vocabulary = db.relationship("Vocabulary",
                            backref=db.backref("terms",cascade="all, delete-orphan", lazy='dynamic'))

    parent_id = db.Column(db.Integer, db.ForeignKey('iroko_terms.id'))
    children = db.relationship("Term", lazy="joined",join_depth=2)

    # any data related to the term
    data = db.Column( JSONType )

    def __str__(self):
        """Representation."""
        return self.name


# TODO: This will be replaced by the graph database, when done....
class TermClasification(db.Model):
    __tablename__ = 'iroko_term_term'
    id = db.Column(db.Integer, primary_key=True)

    # term_class es como el termino <Grupo 1 del MES>
    term_class_id = db.Column(db.Integer(), db.ForeignKey('iroko_terms.id'))

    # term_object es como el termino <Web of Science>
    term_clasified_id = db.Column(db.Integer(), db.ForeignKey('iroko_terms.id'))

    data = db.Column( JSONType )

    def __str__(self):
        """Representation."""
        return self.data_base.name + ' de '+ self.group.name

