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
from iroko.taxonomy.marshmallow import vocabularies_schema, vocabulary_schema, terms_schema, term_schema

from iroko.utils import iroko_json_response, IrokoResponseStatus

api_blueprint = Blueprint(
    'iroko_api_taxonomys',
    __name__,
)


@api_blueprint.route('/vocabularies')
def get_vocabularies():

    result = Vocabulary.query.all()
    if result:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','vocabularies', \
                            vocabularies_schema.dump(result).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, 'vocabularies not found', None, None)



@api_blueprint.route('/terms')
def get_terms_list():

    result = Term.query.all()
    if result:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms', \
                            terms_schema.dump(result).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, 'terms not found', None, None)


@api_blueprint.route('/terms/<vocabulary>')
def get_terms(vocabulary):
    vocab = Vocabulary.query.filter_by(name=vocabulary).first()
    if vocab:
        
        terms = vocab.terms.filter_by(parent_id=None).all()
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms',terms_schema.dump(terms).data)

    return iroko_json_response(IrokoResponseStatus.ERROR, 'no vocab', None, None)


@api_blueprint.route('/terms/<vocabulary>/tree')
def get_terms_tree(vocabulary):
    vocab = Vocabulary.query.filter_by(name=vocabulary).first()
    if vocab:
        terms = vocab.terms.filter_by(parent_id=None).all()
        terms_full = []
        for term in terms:
            terms_full.append(load_term(term))

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms', \
                            {'vocab': vocabulary_schema.dump(vocab).data,\
                            'terms': terms_full})

    return iroko_json_response(IrokoResponseStatus.ERROR, 'no vocab', None, None)


@api_blueprint.route('/term/<uuid>')
def get_term(uuid):
    term = Term.query.filter_by(uuid=uuid).first()
    if term:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','terms', load_term(term))
    return iroko_json_response(IrokoResponseStatus.ERROR, 'no term', None, None)        


def load_term(term):
    children = []
    for child in term.children:
        children.append(load_term(child))
    return {'term': term_schema.dump(term).data, 'children':children}