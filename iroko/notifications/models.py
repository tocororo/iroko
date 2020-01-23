# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017, 2018 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Iroko Notification Admin models."""

from datetime import datetime
from invenio_accounts.models import User
from sqlalchemy import and_, or_
from sqlalchemy_utils.models import Timestamp
from sqlalchemy_utils.types import UUIDType, JSONType
from enum import Enum
import uuid

from invenio_db import db

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
    data = db.Column( JSONType )


    # def __str__(self):
    #     """Representation."""
    #     return self.description

