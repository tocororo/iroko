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

from iroko.taxonomy.models import Vocabulary, Term
from iroko.taxonomy.marshmallow import vocabulary_schema_many, vocabulary_schema, term_schema_many, term_schema

from iroko.utils import iroko_json_response, IrokoResponseStatus

from iroko.taxonomy.api import Vocabularies, Terms

api_blueprint = Blueprint(
    'iroko_api_taxonomys',
    __name__,
)


#TODO: Need authentication
@api_blueprint.route('/vocabulary/<id>', methods=['GET'])
def vocabulary_get(id):

    # FIXME: get current user!!!!
    user = None

    msg, vocab = Vocabularies.get_vocabulary(id)
    if vocab:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'vocabulary', \
                            vocabulary_schema.dump(vocab).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/vocabulary/<id>/edit', methods=['POST'])
def vocabulary_edit(id):

    # FIXME: get current user!!!!
    user = None
    if not request.is_json:
        return {"message": "No JSON data provided"}, 400
    input_data = request.json

    msg, vocab = Vocabularies.edit_vocabulary(id, input_data)
    if vocab:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'vocabulary', \
                        vocabulary_schema.dump(vocab).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/vocabulary/new', methods=['POST'])
def vocabulary_new():

    # FIXME: get current user!!!!
    user = None

    if not request.is_json:
        return {"message": "No JSON data provided"}, 400

    input_data = request.json

    msg, vocab = Vocabularies.new_vocabulary(input_data)
    if vocab:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'vocabulary', \
                        vocabulary_schema.dump(vocab).data)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/vocabularies')
def get_vocabularies():
    """
    List all vocabularies
    """
    result = Vocabulary.query.all()
    if result:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','vocabularies', \
                            vocabulary_schema_many.dump(result).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, 'vocabularies not found', None, None)


@api_blueprint.route('/terms')
def get_terms_list():
    """List all terms """
    result = Term.query.all()
    if result:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms', \
                            term_schema_many.dump(result).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, 'terms not found', None, None)


@api_blueprint.route('/vocabulary/<vocabulary>/terms')
def get_terms(vocabulary):
    """List the first level o the terms in a vocabulary """

    vocab = Vocabulary.query.filter_by(id=vocabulary).first()
    if vocab:

        terms = vocab.terms.filter_by(parent_id=None).all()
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms',term_schema_many.dump(terms).data)

    return iroko_json_response(IrokoResponseStatus.ERROR, 'no vocab', None, None)


@api_blueprint.route('/vocabulary/<vocabulary>/terms/any')
def get_terms_any(vocabulary):
    """List the first level o the terms in a vocabulary """

    vocab = Vocabulary.query.filter_by(id=vocabulary).first()
    if vocab:

        terms = vocab.terms.all()
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms',term_schema_many.dump(terms).data)

    return iroko_json_response(IrokoResponseStatus.ERROR, 'no vocab', None, None)


@api_blueprint.route('/vocabulary/<vocabulary>/terms/tree')
def get_terms_tree(vocabulary):
    """List all the terms in a vocabulary, in a tree """

    vocab = Vocabulary.query.filter_by(id=vocabulary).first()
    if vocab:
        terms = vocab.terms.filter_by(parent_id=None).all()
        terms_full = []
        for term in terms:
            terms_full.append(dump_term(term))

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms', \
                            {'vocab': vocabulary_schema.dump(vocab).data,\
                            'terms': terms_full})

    return iroko_json_response(IrokoResponseStatus.ERROR, 'no vocab', None, None)


#TODO: Need authentication
@api_blueprint.route('/term/<id>/edit', methods=['POST'])
def term_edit(id):

    # FIXME: get current user!!!!
    user = None
    if not request.is_json:
        return {"message": "No JSON data provided"}, 400
    input_data = request.json
    print(input_data)
    msg, term = Terms.edit_term(id, input_data)
    if term:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'term', \
                        term_schema.dump(term).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/term/new', methods=['POST'])
def term_new():

    # FIXME: get current user!!!!
    user = None
    if not request.is_json:
        return {"message": "No JSON data provided"}, 400

    input_data = request.json

    msg, term = Terms.new_term(input_data)
    if term:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        msg,'term', \
                        term_schema.dump(term).data)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)

# TODO: Add POST/PUT for term
@api_blueprint.route('/term/<uuid>')
def term_get(uuid):
    """Get a term given the uuid """

    msg, term = Terms.get_term(uuid)
    if term:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            msg,'term', \
                            term_schema.dump(dump_term(term)).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


#TODO: Need authentication
@api_blueprint.route('/term/<uuid>/delete', methods=['DELETE'])
def term_delete(uuid):

    # FIXME: get current user!!!!
    user = None
        
    try:
        msg, deleted = Terms.delete_term(uuid)
        if deleted:
            return iroko_json_response(IrokoResponseStatus.SUCCESS, msg,'term', {})
    except Exception as e:
        msg = str(e)
    
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


def dump_term(term):
    """ helper function to load terms children"""

    children = []
    for child in term.children:
        children.append(dump_term(child))
    return {'term': term_schema.dump(term).data, 'children':children}


