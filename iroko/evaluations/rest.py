# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

"""Iroko evaluations api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request
from flask_login import current_user
from invenio_oauth2server import require_api_auth

from iroko.evaluations.api import Evaluations
from iroko.evaluations.marshmallow import evaluation_schema, evaluation_schema_many
from iroko.evaluations.models import Evaluation
from iroko.evaluations.permissions import evaluation_viewed_permission_factory
from iroko.utils import IrokoResponseStatus, iroko_json_response

api_blueprint = Blueprint(
    'iroko_api_evaluations',
    __name__,
    url_prefix='/evaluation'
    )


@api_blueprint.route('/list')
@require_api_auth()
def get_evaluations():
    try:
        """
        List all evaluations
        """
        count = int(request.args.get('size')) if request.args.get('size') else 10
        page = int(request.args.get('page')) if request.args.get('page') else 1

        if page < 1:
            page = 1
        offset = count * (page - 1)
        limit = offset + count

        result = Evaluation.query.filter_by(receiver_id=current_user.id).order_by('viewed').all()
        result1 = Evaluation.query.filter_by(receiver_id=current_user.id, viewed=False).all()

        count_not_viewed = len(result1)
        count_total = len(result)

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            'ok', 'evaluations', \
            {
                'data': evaluation_schema_many.dump(result[offset:limit]),
                'total': count_total, 'total_not_view': count_not_viewed
                }
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/<id>', methods=['GET'])
@require_api_auth()
def evaluation_get(id):
    try:
        user = None

        msg, notif = Evaluations.get_evaluation(id)
        if not notif:
            raise Exception('Evaluation not found')

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            msg, 'evaluation', \
            evaluation_schema.dump(notif)
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/receiver/<id>', methods=['GET'])
@require_api_auth()
def evaluation_get_receiver(id):
    try:
        user = None

        msg, notif = Evaluations.get_evaluation_receiver(id)
        if not notif:
            raise Exception('Evaluation not found')

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            msg, 'evaluation', \
            evaluation_schema_many.dump(notif)
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


# TODO: Need authentication
@api_blueprint.route('/edit/<id>', methods=['POST'])
@require_api_auth()
def evaluation_edit(id):
    # FIXME: get the user is trying to perform this action!!!!
    try:
        user = None
        if not request.is_json:
            raise Exception('No JSON data provided')

        input_data = request.json

        msg, notif = Evaluations.edit_evaluation(id, input_data)
        if not notif:
            raise Exception(msg)

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            msg, 'evaluation', \
            evaluation_schema.dump(notif)
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


# TODO: Need authentication
@api_blueprint.route('/viewed/<id>')
@require_api_auth()
def evaluation_viewed(id):
    # FIXME: get the user is trying to perform this action!!!!
    try:
        with evaluation_viewed_permission_factory({'id': id}).require():
            msg, notif = Evaluations.viewed_evaluation(id)
            if not notif:
                raise Exception('Evaluations not found')

            return iroko_json_response(
                IrokoResponseStatus.SUCCESS, \
                msg, 'evaluation', \
                evaluation_schema.dump(notif)
                )

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


# TODO: Need authentication
@api_blueprint.route('/new', methods=['POST'])
@require_api_auth()
def evaluation_new():
    # FIXME: get the user is trying to perform this action!!!!
    try:
        user = None

        if not request.is_json:
            raise Exception('No JSON data provided')

        input_data = request.json

        msg, notif = Evaluations.new_evaluation(input_data)
        if not notif:
            raise Exception(msg)

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            msg, 'evaluation', \
            evaluation_schema.dump(notif)
            )

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
