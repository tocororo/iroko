# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016, 2018 CERN.
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

"""Iroko notifications api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json
from invenio_oauth2server import require_api_auth
from flask_login import current_user

from iroko.notifications.models import Notification
from iroko.notifications.marshmallow import notification_schema_many, notification_schema

from iroko.utils import iroko_json_response, IrokoResponseStatus

from iroko.notifications.api import Notifications

api_blueprint = Blueprint(
    'iroko_api_notifications',
    __name__,
    url_prefix='/noti'
)

@api_blueprint.route('/notifications')
@require_api_auth()
def get_notifications():
    """
    List all notifications
    """
    print('entra')
    result = Notifications.query.all()
    if result:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','notifications', \
                            notification_schema_many.dump(result))
    return iroko_json_response(IrokoResponseStatus.ERROR, 'notifications not found', None, None)


@api_blueprint.route('/notification/<id>', methods=['GET'])
def notification_get(id):

    user = None

    msg, notif = Notifications.get_notification(id)
    if notif:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'notification', \
                            notification_schema.dump(notif))
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/notification/<id>/edit', methods=['POST'])
def notification_edit(id):

    # FIXME: get the user is trying to perform this action!!!!
    user = None
    if not request.is_json:
        return {"message": "No JSON data provided"}, 400
    input_data = request.json

    msg, notif = Notifications.edit_notification(id, input_data)
    if notif:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'notification', \
                        notification_schema.dump(notif))
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/notification/new', methods=['POST'])
def notification_new():

    # FIXME: get the user is trying to perform this action!!!!
    user = None

    if not request.is_json:
        return {"message": "No JSON data provided"}, 400

    input_data = request.json

    msg, notif = Notifications.new_notification(input_data)
    if notif:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'notification', \
                        notification_schema.dump(notif))

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


