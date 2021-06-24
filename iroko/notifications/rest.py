# -*- coding: utf-8 -*-

#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

"""Iroko notifications api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request
from flask_login import current_user
from invenio_oauth2server import require_api_auth

from iroko.notifications.api import Notifications
from iroko.notifications.marshmallow import notification_schema_many, notification_schema
from iroko.notifications.models import Notification
from iroko.notifications.permissions import notification_viewed_permission_factory
from iroko.utils import iroko_json_response, IrokoResponseStatus

api_blueprint = Blueprint(
    'iroko_api_notifications',
    __name__,
    url_prefix='/notification'
)


@api_blueprint.route('/list')
@require_api_auth()
def get_notifications():
    try:
        """
        List all notifications
        """
        count = int(request.args.get('size')) if request.args.get('size') else 10
        page = int(request.args.get('page')) if request.args.get('page') else 1

        if page < 1:
            page = 1
        offset = count * (page - 1)
        limit = offset + count

        result = Notification.query.filter_by(receiver_id=current_user.id).order_by('viewed').all()
        result1 = Notification.query.filter_by(receiver_id=current_user.id, viewed=False).all()

        count_not_viewed = len(result1)
        count_total = len(result)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                   'ok', 'notifications', \
                                   {'data':           notification_schema_many.dump(result[offset:limit]),
                                    'total':          count_total, 'total_not_view': count_not_viewed
                                   })
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
                                   msg, 'notification', \
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
                                   msg, 'notification', \
                                   notification_schema_many.dump(notif))
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


# TODO: Need authentication
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
                                   msg, 'notification', \
                                   notification_schema.dump(notif))
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


# TODO: Need authentication
@api_blueprint.route('/viewed/<id>')
@require_api_auth()
def notification_viewed(id):
    # FIXME: get the user is trying to perform this action!!!!
    try:
        with notification_viewed_permission_factory({'id': id}).require():
            msg, notif = Notifications.viewed_notification(id)
            if not notif:
                raise Exception('Notifications not found')

            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                       msg, 'notification', \
                                       notification_schema.dump(notif))

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


# TODO: Need authentication
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
                                   msg, 'notification', \
                                   notification_schema.dump(notif))

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
