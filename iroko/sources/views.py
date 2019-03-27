
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json
from sqlalchemy import and_, or_, not_
from iroko.sources.models import Sources, TermSources
from iroko.taxonomy.models import Term
from iroko.sources.marshmallow import sources_schema

api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
)


@api_blueprint.route('/sources')
def get_sources():
    """."""

    limit = request.args.get('limit')
    offset = request.args.get('offset')
    title = request.args.get('title')

    # tids = request.args.get('terms')
    # termsources = TermSources.query.filter(TermSources.term_id in tids).group_by(TermSources.sources_id).limit(limit).offset(offset)
    if not limit: 
        limit = 5
    if not offset:
        offset = 0
    
    query = []
    if title:
        query.append(Sources.name.ilike('%'+title+'%'))
    
    result = Sources.query.filter(and_(*query)).limit(limit).offset(offset).all()
    return jsonify(sources_schema.dump(result))


@api_blueprint.route('/sources/count')
def get_sources_count():
    """retorna la cantidad de sources"""
    result = Sources.query.count()
    return jsonify({'count':result})

@api_blueprint.route('/sources/<uuid>')
def get_source_by_id(uuid):
    src = Sources.query.filter_by(uuid=uuid).first()
    if src:
        # terms = terms_schema.dump(vocab.terms)
        return jsonify({'source': sources_schema.dump(src)})
    return jsonify({'source': 'source not found'})

@api_blueprint.route('/sources/term/<uuid>')
def get_sources_by_term_uuid(uuid):
    '''Los sources que estan asociados a un termino'''
    Term
    term = Term.query.filter_by(uuid=uuid).first()
    if term:
         # terms = terms_schema.dump(vocab.terms)
        return jsonify(sources_schema.dump(term.sources))
        # return jsonify(sources_schema.dump(src.sources))
    return jsonify({'term': 'source not found'})



@api_blueprint.route('/sources')
def get_sources_by_term_id(id):
    '''Los sources que estan asociados a un termino'''
    
    terms = request.args.get('terms')

    TermSources.query.filter_by(id=id)

    term = Term.query.filter_by(uuid=uuid).first()
    if term:
         # terms = terms_schema.dump(vocab.terms)
        return jsonify(sources_schema.dump(term.sources))
        # return jsonify(sources_schema.dump(src.sources))
    return jsonify({'term': 'source not found'})
