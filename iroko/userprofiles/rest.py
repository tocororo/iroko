# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko UserProfile api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request
from flask_login import current_user
from invenio_accounts.models import User
from invenio_oauth2server import require_api_auth

from iroko.userprofiles import UserProfile
from iroko.userprofiles.marshmallow import user_schema_many, userprofile_schema
from iroko.utils import IrokoResponseStatus, iroko_json_response
from .views import init_common

api_blueprint = Blueprint(
    'iroko_api_userprofiles',
    __name__,
    )


@api_blueprint.record_once
def init_api(state):
    """Post initialization for API application."""
    init_common(state.app)


@api_blueprint.route('/me', methods=['GET'])
# @require_keycloak_auth(require_token=True, scopes_required=['openid'])
@require_api_auth()
def get_user_info():
    try:
        biography = ""
        institution_name = ""
        institution_id = 0
        institution_rol = ""

        profile = UserProfile.get_or_create_by_userid(current_user.get_id())

        # print("en me", profile)
        # if current_userprofile_json_metadata:
        #     biography = current_userprofile_json_metadata["biography"]
        #     msg, institution = Terms.get_term_by_id(current_userprofile_json_metadata[
        #     "institution_id"])
        #     if institution:
        #         institution_name = institution.name
        #         institution_id = institution.id
        #     institution_rol = current_userprofile_json_metadata["institution_rol"]

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            'ok', 'userprofile', \
            userprofile_schema.dump(profile)
            # {
            #     'email': current_user.email,
            #     'id': current_user.id,
            #     'username': current_userprofile.username,
            #     'full_name':current_userprofile.full_name,
            #     'biography':biography,
            #     'institution_id':institution_id,
            #     'institution':institution_name,
            #     'institution_rol':institution_rol,
            # }
            )
    except Exception as e:
        raise e
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/users/search', methods=['GET'])
@require_api_auth()
def get_users_by_email():
    try:
        count = int(request.args.get('size')) if request.args.get('size') else 10
        page = int(request.args.get('page')) if request.args.get('page') else 1
        query = str(request.args.get('query')) if request.args.get('query') else ''
        if page < 1:
            page = 1
        offset = count * (page - 1)
        limit = offset + count

        users = User.query.filter(User.email.like('%{0}%'.format(query))).all()

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            'ok',
            'users',
            user_schema_many.dump(users[offset:limit])
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


