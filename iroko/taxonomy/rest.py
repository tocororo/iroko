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

"""Iroko taxonomy api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json
from flask_login import current_user
from flask_principal import PermissionDenied

from invenio_oauth2server import require_api_auth

from iroko.taxonomy.models import Vocabulary, Term
from iroko.taxonomy.marshmallow import vocabulary_schema_many, vocabulary_schema, term_schema_many, term_schema

from iroko.utils import iroko_json_response, IrokoResponseStatus

from iroko.taxonomy.api import Vocabularies, Terms, get_current_user_permissions
from iroko.taxonomy.permissions import vocabulary_editor_permission_factory
from iroko.decorators import taxonomy_admin_required


api_blueprint = Blueprint(
    'iroko_api_taxonomys',
    __name__,
    url_prefix='/taxonomy'
)

@api_blueprint.route('/vocabulary/list')
def get_vocabularies():
    """
    List all vocabularies
    """
    try:
        result = Vocabularies.get_vocabularies()
        if not result:
            raise Exception('Vocabularies not found')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok','vocabularies', vocabulary_schema_many.dump(result))

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/vocabulary/<int:id>', methods=['GET'])
def vocabulary_get(id):
    msg = ''
    try:
        msg, vocab = Vocabularies.get_vocabulary(id)
        if not vocab:
            raise Exception('Not vocabulary found')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'vocabulary', \
                            vocabulary_schema.dump(vocab))

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/vocabulary/edit/<int:id>', methods=['POST'])
@require_api_auth()
@taxonomy_admin_required
def vocabulary_edit(id):
    print(current_user)
    msg = ''
    try:

        if not request.is_json:
            raise Exception('No JSON data provided')

        input_data = request.json

        msg, vocab = Vocabularies.edit_vocabulary(id, input_data)
        if not vocab:
            raise Exception(msg)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'vocabulary', \
                            vocabulary_schema.dump(vocab))

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/vocabulary/new', methods=['POST'])
@require_api_auth()
@taxonomy_admin_required
def vocabulary_new():
    msg = ''
    try:
        if not request.is_json:
            raise Exception('No JSON data provided')

        input_data = request.json
        msg, vocab = Vocabularies.new_vocabulary(input_data)

        if not vocab:
            raise Exception(msg)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'vocabulary', \
                        vocabulary_schema.dump(vocab))
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/term/list')
def get_terms_list():
    """List all terms """
    try:
        result =  Terms.get_terms()

        if not result:
            raise Exception('No terms found')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                'ok','terms', \
                                term_schema_many.dump(result))
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/term/list/<vocabulary_id>')
def get_terms(vocabulary_id):
    """Get all terms of a vocabulary in a list """
    try:
        msg, terms = Terms.get_terms_by_vocab(vocabulary_id)
        return iroko_json_response(IrokoResponseStatus.SUCCESS,'ok','terms',term_schema_many.dump(terms))
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/term/tree/<vocabulary_id>/')
def get_terms_tree(vocabulary_id):
    """List all the terms in a vocabulary, in a tree """

    try:
        msg, vocab, terms_full = Terms.get_terms_tree_by_vocabulary(vocabulary_id)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms', \
                            {'vocab': vocabulary_schema.dump(vocab),\
                            'terms': terms_full})
    except Exception as e:
        print(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/term/<uuid>')
def term_get(uuid):
    """Get a term given the uuid """
    try:
        msg, term = Terms.get_term(uuid)
        if not term:
            raise Exception(msg)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, msg,'term', Terms.dump_term(term))

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/term/edit/<uuid>', methods=['POST'])
@require_api_auth()
def term_edit(uuid):

    msg = ''
    try:
        msg, term = Terms.get_term(uuid)
        print(term)
        if not term:
            raise Exception(msg)

        with vocabulary_editor_permission_factory({'id': term.vocabulary_id}).require():
            print(term.vocabulary_id)
            # user = current_user
            if not request.is_json:
                raise Exception("No JSON data provided")

            input_data = request.json
            print(input_data)
            msg, term = Terms.edit_term(term, input_data)
            if not term:
                raise Exception(msg)

            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                msg,'term', \
                                term_schema.dump(term))
    except PermissionDenied as err:
        msg = 'Permission denied for editing term'
    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/term/delete/<uuid>', methods=['DELETE'])
@require_api_auth()
def term_delete(uuid):
    try:
        msg, term = Terms.get_term(uuid)
        with vocabulary_editor_permission_factory({'id': term.vocabulary_id}).require():
            msg, deleted = Terms.delete_term(uuid)
            if deleted:
                return iroko_json_response(IrokoResponseStatus.SUCCESS, msg,'term', {})
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/term/new', methods=['POST'])
@require_api_auth()
def term_new():

    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json
        
        with vocabulary_editor_permission_factory({'id': input_data['vocabulary_id']}).require():
            msg, term = Terms.new_term(input_data)
            if not term:
                raise Exception(msg)
            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'term', \
                            term_schema.dump(term))

    except PermissionDenied as err:
        msg = 'Permission denied for adding term'
    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)



@api_blueprint.route('/taxonomy/user/permissions')
@require_api_auth()
def taxonomy_current_user_permissions():
    msg = ''
    try:
        actions, vocabs  = get_current_user_permissions()
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'permissions',
            {actions:vocabs}
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)



