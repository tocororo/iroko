# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko Notification Admin models."""

import uuid
from enum import Enum

from invenio_accounts.models import User
from invenio_db import db
from sqlalchemy_utils.types import JSONType, UUIDType


# TODO: anndir estado START

class EvaluationState(Enum):
    INITIAL = "initial"
    PROCESSING = "processing"
    FINISH = "finished"
    ERROR = "error"
    START = "start"

class Evaluation(db.Model):
    """Define a Notification"""

    __tablename__ = 'iroko_evaluation'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType, default=uuid.uuid4)
    state = db.Column(db.Enum(EvaluationState))
    datetime = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String)

    entity_name = db.Column(db.String)
    entity_type = db.Column(db.String)
    entity_id_type = db.Column(db.String)
    entity_id_value = db.Column(db.String)

    methodology_schema = db.Column(db.String)
    methodology_name = db.Column(db.String)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            User.id, name='fk_iroko_evaluations_user_id'
            )
        )
    user = db.relationship(
        User, backref=db.backref(
            'evaluations', cascade='all, delete-orphan'
            )
        )


    #instancia de la evaluacion
    data = db.Column(JSONType)
