# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko Notification Admin models."""

from enum import Enum
import uuid

from invenio_accounts.models import User
from invenio_db import db
from sqlalchemy_utils.types import JSONType, UUIDType

# TODO: add data field to Notification and Term

class EvaluationState(Enum):
    INITIAL = "initial"
    PROCESSING = "processing"
    FINISH = "finished"
    ERROR = "error"


class Evaluation(db.Model):
    """Define a Notification"""

    __tablename__ = 'iroko_notification'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType, default=uuid.uuid4)
    state = db.Column(db.Enum(EvaluationState))
    datetime = db.Column(db.Datetime) #TODO: esto puede ser un error
    notes = db.Column(db.String)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            User.id, name='fk_iroko_notifications_user_id'
            )
        )
    user = db.relationship(
        User, backref=db.backref(
            'evaluations', cascade='all, delete-orphan'
            )
        )
    #instancia de la evaluacion
    data = db.Column(JSONType)