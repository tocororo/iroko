import uuid
import enum

from invenio_db import db
from sqlalchemy_utils.types import UUIDType, JSONType

# from  iroko.modules.sources.models import Sources

class HarvestedSource(db.Model):
    """The sources harvested"""

    __tablename__ = 'iroko_harvestsources'

    id = db.Column(db.Integer, primary_key=True)

    source_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_sources.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    source = db.relationship("Sources", 
                            backref=db.backref("harvested_items",cascade="all, delete-orphan", lazy='dynamic'))
    rundate = db.Column(db.DateTime, default=datetime.datetime(year=1900, month=1, day=1), nullable=True)



class HarvestedItemStatus(enum.Enum):

    ERROR = "ERROR"
    HARVESTED = "HARVESTED"
    SCHEMA_VALID = "SCHEMA_VALID"
    RECORDED = "RECORDED"
    RECORD_VALID = "SCHEMA_VALID"
    ENRICHED = "ENRICHED"


class HarvestedItem(db.Model):
    """The items harvested"""

    __tablename__ = 'iroko_harvestitems'

    id = db.Column(db.Integer, primary_key=True)

    source_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_sources.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    source = db.relationship("Sources", 
                            backref=db.backref("harvested_items",cascade="all, delete-orphan", lazy='dynamic'))

    identifier = db.Column(db.String, nullable=False)

    record = db.Column(UUIDType, default=uuid.uuid4)

    status = db.Column(db.Enum(HarvestedItemStatus))

    harvesting_data = db.Column(JSONType)

    def __str__(self):
        """Representation."""
        return self.identifier
