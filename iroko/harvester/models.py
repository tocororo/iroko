
import enum
from sqlalchemy_utils.types import UUIDType, JSONType
from invenio_db import db
from iroko.sources.models import Source

class HarvestType(enum.Enum):
    OAI = "OAI-PMH"
    SWORD = "SWORD"
    CUSTOM = "CUSTOM"


class HarvestedItemStatus(enum.Enum):

    # se elimino el item en la fuente
    DELETED = "DELETED"
    # ocurrio algun error en alguna de las fases
    ERROR = "ERROR"
    # se recolecto el item y se validaron los schemas
    HARVESTED = "HARVESTED"
    # se inserto el item en un IrokoRecord
    RECORDED = "RECORDED"
    # se enrriquecio el record asociado
    ENRICHED = "ENRICHED"


class Repository(db.Model):
    """Repository is the information of the Source related to its condition of a repository, the harvest data, etc...is here"""

    __tablename__ = 'iroko_source_repositories'

    id = db.Column( db.Integer, primary_key=True)

    source_id = db.Column(db.Integer, db.ForeignKey(Source.id, name='fk_iroko_source_repository_source_id'))
    """ID of Source for this inclusion."""

    source = db.relationship("Source", backref=db.backref("repository",cascade="all, delete-orphan", lazy='dynamic'))

    harvest_type = db.Column(db.Enum(HarvestType))
    harvest_endpoint = db.Column(db.String)
    last_harvest_run = db.Column(db.DateTime, nullable=True)
    identifier = db.Column(db.String)
    status = db.Column(db.Enum(HarvestedItemStatus))
    error_log = db.Column(db.String)

    data = db.Column( JSONType )
    """Any relevant data, dependent of the harvest_type, this could mean one thing. Eg, for oai-pmh the information about the set could be here."""


class HarvestedItem(db.Model):
    """The items harvested from a repository"""

    __tablename__ = 'iroko_harvest_items'

    id = db.Column(db.Integer, primary_key=True)

    repository_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_sources.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    repository = db.relationship("Source", backref=db.backref("harvested_items"))

    # el identificador en el repo asociado
    identifier = db.Column(db.String, nullable=False)

    # el uuid del iroko record asociado
    record = db.Column(UUIDType, nullable=True)

    status = db.Column(db.Enum(HarvestedItemStatus))
    error_log = db.Column(db.String)

    data = db.Column( JSONType )
    """Any other relevant data to be used in the future could be here."""

    def __str__(self):
        """Representation."""
        return self.identifier
