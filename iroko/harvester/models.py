
import enum
from sqlalchemy_utils.types import UUIDType

from invenio_db import db


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

    def __str__(self):
        """Representation."""
        return self.identifier
