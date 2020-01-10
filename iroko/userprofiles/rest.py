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

from flask import Blueprint, jsonify, request, json
from flask_login import current_user
from invenio_oauth2server import require_api_auth
from iroko.userprofiles import models, marshmallow, api
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
    return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok', 'userprofile', \
                            { 'email': current_user.email, 'id': current_user.id })
