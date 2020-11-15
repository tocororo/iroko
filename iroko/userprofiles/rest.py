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

"""Iroko UserProfile api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request
from flask_login import current_user
from invenio_accounts.models import User
from invenio_oauth2server import require_api_auth

from iroko.userprofiles import UserProfile
from iroko.userprofiles.marshmallow import userprofile_schema, user_schema_many
from iroko.utils import iroko_json_response, IrokoResponseStatus
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
@require_api_auth()
# @require_oauth_scopes(email_scope.id_)
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
        #     msg, institution = Terms.get_term_by_id(current_userprofile_json_metadata["institution_id"])
        #     if institution:
        #         institution_name = institution.name
        #         institution_id = institution.id
        #     institution_rol = current_userprofile_json_metadata["institution_rol"]

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
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
