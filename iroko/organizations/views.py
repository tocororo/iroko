# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# Iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Blueprint definitions."""

from __future__ import absolute_import, print_function

import datetime
from operator import itemgetter
from os.path import splitext

from flask import Blueprint, request, jsonify, abort, current_app
from flask_login import current_user, login_required
from invenio_cache import current_cache
from invenio_oauth2server import require_api_auth
from invenio_oauth2server.models import Client
from invenio_oauth2server.provider import oauth2
from invenio_oauth2server.views.server import error_handler as oauth_error_handler, authorize as oauth_authorized
from invenio_previewer.proxies import current_previewer

from iroko.organizations.api import OrganizationRecord
from iroko.organizations.marshmallow import MetadataSchemaRelIDsV1
from iroko.organizations.serializers import json_v1_response, json_v1, org_json_v1

blueprint = Blueprint(
    'iroko_organizations',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/organizations'
)
"""Blueprint used for loading templates and static assets

The sole purpose of this blueprint is to ensure that Invenio can find the
templates and static files located in the folders of the same names next to
this file.
"""

# #
# # Views
# #
# @blueprint.route('/oauth/cuor/authorize', methods=['GET', 'POST'])
# # @register_breadcrumb(blueprint, '.', _('Authorize application'))
# @login_required
# @oauth_error_handler
# @oauth2.authorize_handler
# def authorize(*args, **kwargs):
#     """View for rendering authorization request."""
#     if request.method == 'GET':
#         client = Client.query.filter_by(
#             client_id=kwargs.get('client_id')
#         ).first()
#
#         if not client:
#             abort(404)
#         internal_apps = current_app.config['INTERNAL_CLIENT_APPS_SECRETS']
#         if client.client_secret in internal_apps:
#             return True
#
#     return oauth_authorized(*args, **kwargs)



#
# Files related template filters.
#
@blueprint.app_template_filter()
def select_preview_file(files):
    """Get list of files and select one for preview."""
    selected = None

    try:
        for f in sorted(files or [], key=itemgetter('key')):
            file_type = splitext(f['key'])[1][1:].lower()
            if file_type in current_previewer.previewable_extensions:
                if selected is None:
                    selected = f
                elif f['default']:
                    selected = f
    except KeyError:
        pass
    return selected

