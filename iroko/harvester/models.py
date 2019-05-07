import uuid
import enum
from sqlalchemy_utils.types import UUIDType, JSONType, ScalarListType

from invenio_db import db
from datetime import datetime

from datetime import datetime

# from  iroko.sources.models import Sources

class RepositoryStatus(enum.Enum):

    ERROR = "ERROR"
    IDENTIFIED = "IDENTIFIED"
    HARVESTED = "HARVESTED"
    RECORDED = "RECORDED"
    ENRICHED = "ENRICHED"


class HarvestedItemStatus(enum.Enum):

    DELETED = "DELETED"
    ERROR = "ERROR"
    HARVESTED = "HARVESTED"
    SCHEMA_VALID = "SCHEMA_VALID"
    RECORDED = "RECORDED"
    ENRICHED = "ENRICHED"


class Repository(db.Model):
    """A Repository is a Source to be harvest"""

    __tablename__ = 'iroko_harvest_repository'

    id = db.Column(db.Integer, primary_key=True)

    source_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_sources.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    last_run = db.Column(db.DateTime, default=datetime(year=1900, month=1, day=1), nullable=True)

    identifier = db.Column(db.String)

    metadata_formats = db.Column(ScalarListType)

    status = db.Column(db.Enum(RepositoryStatus))

    def __str__(self):
        """Representation."""
        return self.identifier

class RepositorySet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repository_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_harvest_repository.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    repository = db.relationship("Repository", backref=db.backref("sets"))
    setSpec = db.Column(db.String)
    setName = db.Column(db.String)

    def __str__(self):
        """Representation."""
        return self.setName


class HarvestedItem(db.Model):
    """The items harvested from a repository"""

    __tablename__ = 'iroko_harvest_items'

    id = db.Column(db.Integer, primary_key=True)

    repository_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_harvest_repository.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    repository = db.relationship("Repository", backref=db.backref("harvested_items"))

    identifier = db.Column(db.String, nullable=False)

    # TODO: default must be set no None
    record = db.Column(UUIDType, default=uuid.uuid4)

    status = db.Column(db.Enum(HarvestedItemStatus))

    setSpec = db.Column(db.String)

    def __str__(self):
        """Representation."""
        return self.identifier
