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

"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json

from iroko.modules.sources.models import Sources, Term_sources

api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
)


@api_blueprint.route('/sources')
def get_sources():
    """."""
    # path = request.args.get('pathname', None)

    result = []
    for src in Sources.query.all():
        result.append({'name': src.name})

    return jsonify(result)

@api_blueprint.route('/sources/<id>')
def get_source_by_id(id):
    result = []
    src = Sources.query.filter_by(name=id).first()
    if vocab is not None:
        for term in vocab.terms:
            result.append(term.to_dict())
    return jsonify(result)