#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import enum

from invenio_db import db
from sqlalchemy_utils.types import JSONType, UUIDType


class HarvestType(enum.Enum):
    OAI = "OAI-PMH"
    SWORD = "SWORD"
    CUSTOM = "CUSTOM"


class HarvestedItemStatus(enum.Enum):
    # the item is deleted in the source
    DELETED = "DELETED"
    # an error
    ERROR = "ERROR"
    # FETCHING
    FETCHING = "FETCHING"
    # item identified
    IDENTIFIED = 'IDENTIFIED'
    # item harvested
    HARVESTED = "HARVESTED"
    # item in a record
    RECORDED = "RECORDED"
    # item enriched
    ENRICHED = "ENRICHED"


class Repository(db.Model):
    """Repository is the information of the Source related to
    its condition of a repository, the harvest data, etc...is here"""

    __tablename__ = 'iroko_source_repositories'

    # id = db.Column( db.Integer, primary_key=True)

    # source_id = db.Column(db.Integer, db.ForeignKey(Source.id,
    # name='fk_iroko_source_repository_source_id'))
    # """ID of Source for this inclusion."""
    #
    # source = db.relationship("Source", backref=db.backref("repository",cascade="all,
    # delete-orphan", lazy='dynamic'))

    source_uuid = db.Column(UUIDType, primary_key=True)

    harvest_type = db.Column(db.Enum(HarvestType))
    harvest_endpoint = db.Column(db.String)
    last_harvest_run = db.Column(db.DateTime, nullable=True)
    identifier = db.Column(db.String)
    status = db.Column(db.Enum(HarvestedItemStatus))
    error_log = db.Column(db.String)

    data = db.Column(JSONType)
    """Any relevant data, dependent of the harvest_type,
    this could mean one thing. Eg, for oai-pmh the information about the set
    could be here."""


class HarvestedItem(db.Model):
    """The items harvested from a repository"""

    __tablename__ = 'iroko_harvest_items'
    __table_args__ = (db.UniqueConstraint(
        'source_uuid',
        'identifier',
        name='identifier_in_repository'
        ),
        )
    id = db.Column(db.Integer, primary_key=True)

    source_uuid = db.Column(
        UUIDType,
        db.ForeignKey(
            'iroko_source_repositories'
            '.source_uuid', ondelete='CASCADE'
            ),
        nullable=False, index=True
        )
    repository = db.relationship(
        "Repository", backref=db.backref(
            'harvested_items'
            )
        )

    """identifier in the repo"""
    identifier = db.Column(db.String, nullable=False)

    # el uuid del iroko record asociado
    record = db.Column(UUIDType, nullable=True)

    status = db.Column(db.Enum(HarvestedItemStatus))
    error_log = db.Column(db.String)

    data = db.Column(JSONType)
    """Any other relevant data to be used in the future could be here."""

    # TODO: add this field
    # last_modified = db.Column(db.DateTime, nullable=False)

    def __str__(self):
        """Representation."""
        return self.identifier
