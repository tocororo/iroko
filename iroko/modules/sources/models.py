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

class Sources(db.Model):
    """Define a Source"""

    __tablename__ = 'sources'

    id = db.Column( db.Integer, primary_key=True)
    uuid = db.Column( db.String, unique=True)
    name = db.Column( db.String, nullable=False, unique=True)
    description = db.Column( db.String )
    source_type = db.Column( db.String )
    data = db.Column( db.String )
    
    term_sources = relationship("Term_sources", back_populates="sources")

    def __str__(self):
        """Representation."""
        return self.name
    
    def to_dict(self):
        return {'name': self.name, 
                'description': self.description,
                'parent': self.term_sources}


class Term_sources(db.Model):
    __tablename__ = 'term_sources'

    term_id = Column( Integer, ForeignKey('taxonomy_term.id'), primary_key=True)
    sources_id = Column( Integer, ForeignKey('sources.id'), primary_key=True)
    data = de.Column( db.String )

    source = relationship("Sources", back_populates="taxonomy_term") 
    term = relationship("Term", back_populates="sources")

