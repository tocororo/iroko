
#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko Taxonomy Admin models."""

import enum
import uuid

from invenio_accounts.models import User
from invenio_db import db
from sqlalchemy_utils.types import UUIDType, JSONType


class SourceInstitutionRole(enum.Enum):
    MAIN = "MAIN"
    COLABORATOR = "COLABORATOR"


class SourcePersonRol(enum.Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    JOURNALMANAGER = "JOURNALMANAGER"
    AUTHOR = "AUTHOR"
    EDITOR = "EDITOR"
    SECTIONEDITOR = "SECTIONEDITOR"
    REVIEWER = "REVIEWER"
    COPYEDITOR = "COPYEDITOR"
    LAYOUTEDITOR = "LAYOUTEDITOR"
    PROOFREADER = "PROOFREADER"  # CORRECTOR DE PRUEBAS
    READER = "READER"


class SourceType(enum.Enum):
    JOURNAL = "JOURNAL"
    STUDENT = "STUDENT"
    POPULARIZATION = "POPULARIZATION"
    REPOSITORY = "REPOSITORY"
    WEBSITE = "WEBSITE"
    OTHER = "OTHER"


class SourceStatus(enum.Enum):
    APPROVED = "APPROVED"
    TO_REVIEW = "TO_REVIEW"
    UNOFFICIAL = 'UNOFFICIAL'


# This class (Source) is deprecated!!!!
class Source(db.Model):
    """Source, fuente, es define una fuente primaria de datos, eg: las revistas.
    Aqui se tiene la informacion basica de la fuente,
    su relacion con la taxonomia y la informacion de la fuente en tanto repositorio de documentos """

    __tablename__ = 'iroko_sources'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False, unique=True)
    source_type = db.Column(db.Enum(SourceType))
    source_status = db.Column(db.Enum(SourceStatus))

    # TODO: decidir sobre esto:  Aunque este repetido, creo que es conveniente poner aqui (y manejar en las apps, en consecuencia), las relaciones con los terminos. En las tablas se pone por facilidad, pero aunque este repetido, a la hora de "editar" un Source, me parece que es mas facil asi..
    data = db.Column(JSONType)
    """The data of the Source, dependent on the source type, including the relationships with Terms"""

    # term_sources = db.relationship("Term_sources", back_populates="sources")

    def __str__(self):
        """Representation."""
        return self.name


# TODO: medium term, este modelo y todas las implicaciones que tiene, en las relaciones de sql
# y en los data que manejamos(source y sourceversion) sera sustituido por "relations",
# un campo en marshmallow que trabajaria con neo4j
class TermSources(db.Model):
    __tablename__ = 'iroko_terms_sources'

    # TODO: Esta relacion deberia hacerse con los UUIDs y no con los IDs
    term_id = db.Column(db.Integer, db.ForeignKey('iroko_terms.id'), primary_key=True)
    sources_id = db.Column(db.Integer, db.ForeignKey('iroko_sources.id'), primary_key=True)
    data = db.Column(JSONType)

    source = db.relationship("Source", backref=db.backref("term_sources"))
    term = db.relationship("Term", backref=db.backref("term_sources"))


class SourceVersion(db.Model):
    """Version de una fuente. Se utiliza para el proceso de inclusion y modificacion de los datos de una fuente. Al solicitar la inclusion de una nueva fuente, un usuario crea una version, posteriormente un editor valida esta version. En otro momento el usuario puede modificar los datos, que deberan ser validados, en todos los casos se crean versiones del source.  Un SourceVersion, no se puede modificar."""

    __tablename__ = 'iroko_source_versions'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        User.id, name='fk_iroko_source_versions_user_id'))
    """ID of user to whom this inclusion belongs."""

    user = db.relationship(User, backref='iroko_source_versions')

    source_uuid = db.Column(UUIDType, nullable=False)

    #
    # source_id = db.Column(db.Integer, db.ForeignKey(
    #     Source.id, name='fk_iroko_source_versions_source_id'))
    # """ID of Source for this inclusion."""
    #
    # source = db.relationship("Source",
    #                          backref=db.backref("versions",
    #                                             cascade="all, delete-orphan",
    #                                             lazy='dynamic',
    #                                             order_by='SourceVersion.created_at.desc()')
    #                          )
    comment = db.Column(db.String)

    # TODO: Creo que es conveniente que aqui se incluyan las relaciones con los terminos (en principio usando IDs)asi, al crear una nueva version, se pueden reflejar los cambios en las bases de datos.
    data = db.Column(JSONType)
    """The data of the Source, dependent on the source type, including the relationships with Terms"""

    created_at = db.Column(db.DateTime)

    is_current = db.Column(db.Boolean)
    """If is the current active version of Source"""

    reviewed = db.Column(db.Boolean)
    """the version is reviewed by some gestor"""

    def __str__(self):
        """Representation."""
        return self.source.name + ' : ' + self.created_at + ' : ' + self.is_current


class SourceRawData(db.Model):
    __tablename__ = 'iroko_source_raw_data'

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String, nullable=False, unique=True)

    # for any data, key is the source of information:
    # 'issn':{...} is the data collected from issn.org
    # 'miar':{...} is the data collected from MIAR
    data = db.Column(JSONType)

    def __str__(self):
        """Representation."""
        return self.identifier

    def set_data_field(self, field_name, field_data):
        if not self.data:
            self.data = dict()
        d = dict(self.data)
        d[field_name] = field_data
        self.data = d
        db.session.commit()

    # def commit_data_field(self, field_name, field_data):
    #     with db.session.begin_nested():
    #         self.set_data_field(field_name, field_data)
    #         db.session.commit(self)

    def get_data_field(self, field_name):
        if field_name not in self.data:
            self.set_data_field(field_name, dict())
        return self.data[field_name]
