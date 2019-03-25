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
import enum
from invenio_db import db

from iroko.modules.taxonomy.models import Term

class SourcesType(enum.Enum):
    JOURNAL = "Journal"
    REPOSITORY = "Repository"
    WEBSITE = "Website"

class HarvestType(enum.Enum):
    OAI = "OAI-PMH"
    SWORD = "SWORD"
    CUSTOM = "CUSTOM"

class Sources(db.Model):
    """Define a Source"""

    __tablename__ = 'iroko_sources'

    id = db.Column( db.Integer, primary_key=True)
    uuid = db.Column(UUIDType, default=uuid.uuid4)
    name = db.Column( db.String, nullable=False, unique=True)
    source_type = db.Column( db.Enum(SourcesType))
    data = db.Column( JSONType )
    
    harvest_type = db.Column(db.Enum(HarvestType))
    harvest_endpoint = db.Column(db.String)
    
    #term_sources = db.relationship("Term_sources", back_populates="sources")

    def __str__(self):
        """Representation."""
        return self.name


class TermSources(db.Model):
    __tablename__ = 'iroko_terms_sources'

    term_id = db.Column( db.Integer, db.ForeignKey('iroko_terms.id'), primary_key=True)
    sources_id = db.Column( db.Integer, db.ForeignKey('iroko_sources.id'), primary_key=True)
    data = db.Column( JSONType )

    source = db.relationship("Sources", backref=db.backref("terms")) 
    term = db.relationship(Term, backref=db.backref("sources"))
