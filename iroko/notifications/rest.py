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
from iroko.notifications.permissions import notification_viewed_permission_factory
from iroko.notifications.models import Notification
from iroko.notifications.marshmallow import notification_schema_many, notification_schema

from iroko.utils import iroko_json_response, IrokoResponseStatus

from iroko.notifications.api import Notifications

api_blueprint = Blueprint(
    'iroko_api_notifications',
    __name__,
    url_prefix='/notification'
)

@api_blueprint.route('/list')
# @require_api_auth()
def get_notifications():
    try:
        """
        List all notifications
        """
        count = int(request.args.get('count')) if request.args.get('count') else 9
        page = int(request.args.get('page')) if request.args.get('page') else 0

        limit = count
        offset = count*page

        result = Notification.query.filter_by(receiver_id = current_user.id).order_by('viewed').all()
        result1 = Notification.query.filter_by(receiver_id = current_user.id,viewed = False).all()
        count_total = len(result1)
        if not result:
            raise Exception('Notification not found')
        
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','notifications', \
                            {'data':notification_schema_many.dump(result[offset:offset+limit]), 'total': count_total})                    
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
                            
    


@api_blueprint.route('/<id>', methods=['GET'])
@require_api_auth()
def notification_get(id):
    try:
        user = None

        msg, notif = Notifications.get_notification(id)
        if not notif:
            raise Exception('Notification not found')
        
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'notification', \
                            notification_schema.dump(notif))
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)

@api_blueprint.route('/receiver/<id>', methods=['GET'])
@require_api_auth()
def notification_get_receiver(id):
    try:
        user = None

        msg, notif = Notifications.get_notification_receiver(id)
        if not notif:
            raise Exception('Notification not found')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'notification', \
                            notification_schema_many.dump(notif))
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/edit/<id>', methods=['POST'])
@require_api_auth()
def notification_edit(id):

    # FIXME: get the user is trying to perform this action!!!!
    try:
        user = None
        if not request.is_json:
            raise Exception('No JSON data provided')

        input_data = request.json

        msg, notif = Notifications.edit_notification(id, input_data)
        if not notif:
            raise Exception(msg)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'notification', \
                        notification_schema.dump(notif))
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/viewed/<id>')
@require_api_auth()
def notification_viewed(id):
    
    # FIXME: get the user is trying to perform this action!!!!
    try:
        with notification_viewed_permission_factory({'id':id}).require():
            msg, notif = Notifications.viewed_notification(id)
            if not notif:
                raise Exception('Notifications not found')

            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'notification', \
                            notification_schema.dump(notif))

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/new', methods=['POST'])
@require_api_auth()
def notification_new():

    # FIXME: get the user is trying to perform this action!!!!
    try:
        user = None

        if not request.is_json:
            raise Exception('No JSON data provided')

        input_data = request.json

        msg, notif = Notifications.new_notification(input_data)
        if not notif:
            raise Exception(msg)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'notification', \
                        notification_schema.dump(notif))
    
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


