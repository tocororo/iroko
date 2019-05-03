
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json, render_template
from sqlalchemy import and_, or_, not_
from iroko.sources.models import Sources, TermSources
from iroko.taxonomy.models import Term
from iroko.sources.marshmallow import sources_schema, sources_schema_full, journal_schema
from invenio_db import db


blueprint = Blueprint(
    'iroko_sources',
    __name__,
    template_folder='templates',
    static_folder='static'
)


api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
)

@blueprint.route('/catalog')
def catalog_app():
    return render_template('catalog.html')


@api_blueprint.route('/sources')
def get_sources():
    """."""

    op = request.args.get('op')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    title = request.args.get('title')
    issn = request.args.get('issn')

    tids = request.args.get('terms')
    terms = []
    if tids:
        tids= tids.split(',')
        term_op = tids[0]    
        if tids[0].lower() is 'and' or tids[0].lower() is 'or':
            del tids[0]    
        terms = tids    
    

    if not limit: 
        limit = 5
    if not offset:
        offset = 0   
    
    their_children = []
    for par_term in terms:
        aux = Term.query.filter_by(id=par_term).first()        
        tchildren = load_term_children_id(aux)
        if tchildren:
            their_children += tchildren
    all_terms = set(their_children + terms)    
    print(all_terms)

    sources=[]        
    tm = TermSources.query.filter(TermSources.term_id.in_(all_terms)).all()
    for t in tm:
        iftitle = check_title(t.source, title) 
        ifissn = check_issn(t.source, issn)     

        andcheck = iftitle and ifissn
        orcheck = iftitle or ifissn
        if andcheck:
            print(t.source.name)
        if (str(op) == 'and' and andcheck) or orcheck:
            sources.append(t.source)    
    
    if sources:    
        return jsonify(sources_schema_full.dump(sources[offset:offset+limit]))        
    return jsonify({'message':'Sources not found'})


def check_title(source, title):
    if not title or title in source.name:
        return True
    return False


def check_rnps(source, rnps):
    if not rnps or rnps in source.rnps:
        return True
    return False


def check_issn(source, issn):
    if not issn or issn in source.data['issn'].values():
        return True
    return False


def get_all_sources(title, limit=10, offset=0):
    query = []
    if title:
        query.append(Sources.name.ilike('%'+title+'%'))
    
    # result = Sources.query.filter(and_(*query)).limit(limit).offset(offset).all()
    # return jsonify(sources_schema.dump(result))


@api_blueprint.route('/sources/count')
def get_sources_count():
    """retorna la cantidad de sources"""
    result = Sources.query.count()
    return jsonify({'count':result})

@api_blueprint.route('/source/id/<id>')
def get_source_by_id(id):    
    src = Sources.query.filter_by(id=id)
    if src:
        # terms = terms_schema.dump(vocab.terms)
        return jsonify({'source': sources_schema.dump(src)})
    return jsonify({'source': 'source not found'})


@api_blueprint.route('/source/uuid/<uuid>')
def get_source_by_uuid(uuid):    
    src = Sources.query.filter_by(uuid=uuid)
    if src:
        # terms = terms_schema.dump(vocab.terms)
        return jsonify({'source': sources_schema.dump(src)})
    return jsonify({'source': 'source not found'})


def load_term_children_id(term):    
    if term.children:
        children = []
        for child in term.children:
            children.append(child.id)
            load_term_children_id(child)
        return children


@api_blueprint.route('/term/sources')
def get_sources_by_term_id():
    '''Los sources que estan asociados a un termino'''
    
    terms = request.args.get('terms').split(',')    
    their_children = []
    for par_term in terms:
        aux = Term.query.filter_by(id=par_term).first()        
        tchildren = load_term_children_id(aux)
        if tchildren:
            their_children += tchildren
    all_terms = set(their_children + terms)
    
    sources=[]        
    tm = TermSources.query.filter(TermSources.term_id.in_(all_terms)).all()
    for t in tm:
        one_source = t.source

        sources.append(one_source)    
    
    if sources:    
        return jsonify(sources_schema.dump(sources))        
    return jsonify({'term': 'source not found'})

