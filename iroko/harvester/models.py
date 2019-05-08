import uuid
import enum
from sqlalchemy_utils.types import UUIDType, JSONType, ScalarListType

from invenio_db import db
from datetime import datetime

from datetime import datetime

# from  iroko.sources.models import Sources

class RepositoryStatus(enum.Enum):

    # algun error en alguna de las fases
    ERROR = "ERROR"
    # el harvester se conecto al repo y obtuvo su identificacion 
    IDENTIFIED = "IDENTIFIED"
    # se recolectaron los items de 
    HARVESTED = "HARVESTED"
    # parsearon los items y se insertaron IrokoRecors
    RECORDED = "RECORDED"
    # se enrriquecieron todos los items asociados a este repo
    ENRICHED = "ENRICHED"


class Repository(db.Model):
    """A Repository is a Source to be harvest"""

    __tablename__ = 'iroko_harvest_repository'

    id = db.Column(db.Integer, primary_key=True)

    source_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_sources.id', ondelete='CASCADE'),
                        nullable=False, index=True)

    # la fecha del ultima cosecha, debe ponerse cuando el repo pasa al status HARVESTED
    last_run = db.Column(db.DateTime, default=datetime(year=1900, month=1, day=1), nullable=True)

    # identificador de la fuente
    identifier = db.Column(db.String)

    # una lista con los metadata formats (dc, nlm, marc, etc...)
    metadata_formats = db.Column(ScalarListType)

    status = db.Column(db.Enum(RepositoryStatus))
    error_log = db.Column(db.String)

    def __str__(self):
        """Representation."""
        return self.identifier

class RepositorySet(db.Model):
    """ Para el campo spec en el Dublin Core
    cada repositorio define sus sets, la idea con esta tabla es tener
    los nombres de cada set, de manera que despues se pueda enrriquecer 
    los items con un vocabulario unico e.g: el tipo de articulo(original, revision, editorial, etc.. )"""
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
                        db.ForeignKey('iroko_harvest_repository.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    repository = db.relationship("Repository", backref=db.backref("harvested_items"))

    # el identificador en el repo asociado
    identifier = db.Column(db.String, nullable=False)

    # el uuid del iroko record asociado 
    record = db.Column(UUIDType, nullable=True)

    status = db.Column(db.Enum(HarvestedItemStatus))
    error_log = db.Column(db.String)

    def __str__(self):
        """Representation."""
        return self.identifier
