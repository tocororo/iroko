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

"""Iroko issn api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json
from invenio_oauth2server import require_api_auth
from flask_login import current_user
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.issn.api import Issn

api_blueprint = Blueprint(
    'iroko_api_issn',
    __name__,
    url_prefix='/issn'
)

@api_blueprint.route('/<name>', methods=['GET'])
# @require_api_auth()
def issn_get(name):
    try:
        user = None
        print('asdasdasdas')
        msg, issn = Issn.get_issn(name)
        if not issn:
            raise Exception('Issn not found')
        
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'issn', \
                            issn)
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)