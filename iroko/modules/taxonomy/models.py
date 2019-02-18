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

from invenio_db import db

class Vocabulary(db.Model):
    """Define a Vocabulary"""

    __tablename__ = 'taxonomy_vocab'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    
    # terms = db.relationship("Term")

    def __str__(self):
        """Representation."""
        return self.name


class Term(db.Model):
    __tablename__ = 'taxonomy_term'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    vocabulary_id = db.Column(db.Integer(),
                        db.ForeignKey('taxonomy_vocab.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    vocabulary = db.relationship("Vocabulary",
                           backref=db.backref("terms",
                                              cascade="all, delete-orphan"))

    parent_id = db.Column(db.Integer, db.ForeignKey('taxonomy_term.id'))
    children = db.relationship("Term")

    def to_dict(self):
        return {'name': self.name, 
                'description': self.description,
                'parent': self.parent_id}
