# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017, 2018 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Iroko Taxonomy Admin models."""

from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy_utils.models import Timestamp
from sqlalchemy_utils.types import UUIDType, JSONType
import uuid

from invenio_db import db

# TODO: add data field to Vocabulary and Term

class Vocabulary(db.Model):
    """Define a Vocabulary"""

    __tablename__ = 'iroko_vocab'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)

    # any data related to the vocabulary
    data = db.Column( JSONType )


    def __str__(self):
        """Representation."""
        return self.name


class Term(db.Model):
    __tablename__ = 'iroko_terms'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    vocabulary_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_vocab.id', ondelete='CASCADE'),
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


class TermClasification(db.Model):
    __tablename__ = 'iroko_term_term'
    id = db.Column(db.Integer, primary_key=True)

    # term_class es como el termino <Grupo 1 del MES>
    term_class_id = db.Column(db.Integer(), db.ForeignKey('iroko_terms.id'))

    # term_object es como el termino <Web of Science>
    term_object_id = db.Column(db.Integer(), db.ForeignKey('iroko_terms.id'))    

    def __str__(self):
        """Representation."""
        return self.data_base.name + ' de '+ self.group.name
    
