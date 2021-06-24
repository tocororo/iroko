# -*- coding: utf-8 -*-

#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko Notification Admin models."""

from enum import Enum

from invenio_accounts.models import User
from invenio_db import db
from sqlalchemy_utils.types import JSONType


# TODO: add data field to Notification and Term

class NotificationType(Enum):
    INFO = "info"
    ERROR = "error"
    ALERT = "alert"


class Notification(db.Model):
    """Define a Notification"""

    __tablename__ = 'iroko_notification'

    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.Enum(NotificationType))
    description = db.Column(db.String)
    emiter = db.Column(db.String)
    viewed = db.Column(db.Boolean, default=False)
    receiver_id = db.Column(db.Integer,
                            db.ForeignKey(
                                User.id, name='fk_iroko_notifications_user_id'))

    receiver = db.relationship(
        User, backref=db.backref(
            'notifications', cascade='all, delete-orphan')
    )
    # any data related to the notification
    data = db.Column(JSONType)

    # def __str__(self):
    #     """Representation."""
    #     return self.description
