
"""Iroko Taxonomy Admin models."""

from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy_utils.models import Timestamp
from sqlalchemy_utils.types import UUIDType, JSONType, ScalarListType
import uuid
import enum
from invenio_db import db

from invenio_accounts.models import User

from iroko.taxonomy.models import Term

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


class SourceType(enum.Enum):
    JOURNAL = "journal"
    STUDENT = "student"
    POPULARIZATION = "popularization"
    REPOSITORY = "repository"
    WEBSITE = "website"


class SourceStatus(enum.Enum):
    APPROVED = "APPROVED"
    TO_REVIEW = "TO_REVIEW"
    UNOFFICIAL = 'UNOFFICIAL'


class HarvestType(enum.Enum):
    OAI = "OAI-PMH"
    SWORD = "SWORD"
    CUSTOM = "CUSTOM"


class Source(db.Model):
    """Source, fuente, es define una fuente primaria de datos, eg: las revistas. Aqui se tiene la informacion basica de la fuente, su relacion con la taxonomia y la informacion de la fuente en tanto repositorio de documentos """

    __tablename__ = 'iroko_sources'

    id = db.Column( db.Integer, primary_key=True)
    uuid = db.Column(UUIDType, default=uuid.uuid4)
    name = db.Column( db.String, nullable=False, unique=True)
    source_type = db.Column( db.Enum(SourceType))
    source_status = db.Column( db.Enum(SourceStatus))

    # TODO: decidir sobre esto:  Aunque este repetido, creo que es conveniente poner aqui (y manejar en las apps, en consecuencia), las relaciones con los terminos. En las tablas se pone por facilidad, pero aunque este repetido, a la hora de "editar" un Source, me parece que es mas facil asi..
    data = db.Column( JSONType )

    #term_sources = db.relationship("Term_sources", back_populates="sources")

    # TODO: Fields related to repository...  at some point, this shoud be in a different model, and a source should have different Repositories.
    repo_harvest_type = db.Column(db.Enum(HarvestType))
    repo_harvest_endpoint = db.Column(db.String)
    repo_last_harvest_run = db.Column(db.DateTime, default=datetime(year=1900, month=1, day=1), nullable=True)
    repo_identifier = db.Column(db.String)
    repo_metadata_formats = db.Column(ScalarListType)
    repo_status = db.Column(db.Enum(RepositoryStatus))
    repo_error_log = db.Column(db.String)

    def __str__(self):
        """Representation."""
        return self.name


class SourceVersion(db.Model):
    """Version de una fuente. Se utiliza para el proceso de inclusion y modificacion de los datos de una fuente. Al solicitar la inclusion de una nueva fuente, un usuario crea una version, posteriormente un editor valida esta version. En otro momento el usuario puede modificar los datos, que deberan ser validados, en todos los casos se crean versiones del source.  Un SourceVersion, no se puede modificar."""

    __tablename__ = 'iroko_source_versions'

    id = db.Column( db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        User.id, name='fk_iroko_source_versions_user_id'))
    """ID of user to whom this inclusion belongs."""

    user = db.relationship(User, backref='iroko_source_versions')

    source_id = db.Column(db.Integer, db.ForeignKey(
        Source.id, name='fk_iroko_source_versions_source_id'))
    """ID of Source for this inclusion."""

    source = db.relationship("Source", backref=db.backref("versions",cascade="all, delete-orphan", lazy='dynamic'))

    comment = db.Column(db.String)

    # TODO: Creo que es conveniente que aqui se incluyan las relaciones con los terminos (en principio usando IDs)asi, al crear una nueva version, se pueden reflejar los cambios en las bases de datos.
    data = db.Column( JSONType )
    """The data of the Source, include the relationships with Terms"""

    created_at = db.Column(db.DateTime)

    is_current = db.Column(db.Boolean)
    """If is the current active version of Source"""

    def __str__(self):
        """Representation."""
        return self.source.name + ' : ' + self.created_at + ' : ' + self.is_current


class RepositorySet(db.Model):
    """ Para el campo spec en el Dublin Core
    cada repositorio define sus sets, la idea con esta tabla es tener
    los nombres de cada set, de manera que despues se pueda enrriquecer
    los items con un vocabulario unico e.g: el tipo de articulo(original, revision, editorial, etc.. )"""

    __tablename__ = 'iroko_repository_sets'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer(),
                        db.ForeignKey('iroko_sources.id', ondelete='CASCADE'),
                        nullable=False, index=True)
    source = db.relationship("Source", backref=db.backref("sets"))
    setSpec = db.Column(db.String)
    setName = db.Column(db.String)

    def __str__(self):
        """Representation."""
        return self.setName


class TermSources(db.Model):
    __tablename__ = 'iroko_terms_sources'

    term_id = db.Column(db.Integer, db.ForeignKey('iroko_terms.id'), primary_key=True)
    sources_id = db.Column(db.Integer, db.ForeignKey('iroko_sources.id'), primary_key=True)
    data = db.Column(JSONType)

    source = db.relationship("Source", backref=db.backref("terms"))
    term = db.relationship("Term", backref=db.backref("sources"))


