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

from iroko.modules.taxonomy.models import Vocabulary, Term
from iroko.modules.taxonomy.marshmallow import vocabularies_schema, vocabulary_schema, terms_schema, term_schema

api_blueprint = Blueprint(
    'iroko_api_taxonomys',
    __name__,
)


@api_blueprint.route('/vocabularies')
def get_vocabularies():
    """."""
    # path = request.args.get('pathname', None)

    result = Vocabulary.query.all()
    return jsonify(vocabularies_schema.dump(result))


@api_blueprint.route('/terms/<vocabulary>')
def get_terms(vocabulary):
    vocab = Vocabulary.query.filter_by(name=vocabulary).first()
    if vocab:
        deep = request.args.get('deep')
        terms = vocab.terms.filter_by(parent_id=None).all()
        if deep:
            terms_full = []
            for term in terms:
                terms_full.append(load_term(term))
            return jsonify({'vocab': vocabulary_schema.dump(vocab), 
                        'terms': terms_full})
        else:
            return jsonify({'vocab': vocabulary_schema.dump(vocab), 
                        'terms': terms_schema.dump(terms)})
    return jsonify({'vocab': 'no vocab'})


@api_blueprint.route('/term/<uuid>')
def get_term(uuid):
    term = Term.query.filter_by(uuid=uuid).first()
    if term:
        return jsonify(load_term(term))


def load_term(term):
    children = []
    for child in term.children:
        children.append(load_term(child))
    return {'term': term_schema.dump(term), 'children':children}