
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json, render_template
from sqlalchemy import and_, or_, not_
from iroko.sources.models import Sources, TermSources
from iroko.taxonomy.models import Term
from iroko.sources.marshmallow import sources_schema, sources_schema_full, journal_schema, SourcesSchema
from invenio_db import db

from iroko.utils import iroko_json_response, IrokoResponseStatus


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
    return render_template('index.html')


@api_blueprint.route('/sources')
def get_sources():

    and_op = True if request.args.get('op') and request.args.get('op') == 'and' else False

    count = int(request.args.get('count')) if request.args.get('count') else 10
    page = int(request.args.get('page')) if request.args.get('page') else 0

    limit = count
    offset = count*page
    tids = request.args.get('terms')
    
    data_args = {
        'title' : str(request.args.get('title')),
        'description': str(request.args.get('description')),
        'url': str(request.args.get('url')),
        'issn': str(request.args.get('issn')),
        'rnps': str(request.args.get('rnps')),
        'year_start': str(request.args.get('year_start')),
        'year_end': str(request.args.get('year_end'))
    }
    
    terms = []
    if tids:
        tids= tids.split(',')
        term_op = tids[0]    
        if tids[0].lower() is 'and' or tids[0].lower() is 'or':
            del tids[0]    
        terms = tids   
    print(tids, terms)
    all_terms = load_terms_tree(terms)

    result=[]
    ask_terms = len(all_terms) > 0
    if ask_terms:
        sources = TermSources.query.filter(TermSources.term_id.in_(all_terms)).order_by(text('iroko_sources.name')).all()
    else:
        sources = Sources.query.order_by('name').all()

    for item in sources:
        source = item.source if ask_terms else item
        if is_like(source, data_args, and_op):
            result.append(source)
    
    if result:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': sources_schema_full.dump(result[offset:offset+limit]).data,\
                         'count': len(result)})
    return iroko_json_response(IrokoResponseStatus.ERROR, 'Sources not found', None, None)

def no_params(param_data):
    return param_data['title'] == 'None' and \
        param_data['description'] == 'None' and \
        param_data['url'] == 'None' and \
        param_data['issn'] == 'None' and \
        param_data['rnps'] == 'None' and \
        param_data['year_start'] == 'None' and \
        param_data['year_end'] == 'None' 

def is_like(source, data, and_op):
    """ esto es ineficiente... pero es lo que hay.. por el momento.. 
    solo debe usarse para la lista de revistas que no pasa de 300"""
    
    if no_params(data):
        return True

    title = data['title'].lower() in str(source.name).lower()
    description = data['description'] in source.data['description'] \
        if 'description' in source.data else False
    url = data['url'] in source.data['url'] if 'url' in source.data else False

    issn = False
    if 'issn' in source.data:
        issn_p = data['issn'].lower() in source.data['issn']['p'].lower() if 'p' in source.data['issn'] else False
        issn_e = data['issn'].lower() in source.data['issn']['e'].lower() if 'e' in source.data['issn']else False
        issn_l = data['issn'].lower() in source.data['issn']['l'].lower() if 'l' in source.data['issn']else False
        issn = issn_p or issn_e or issn_l

    rnps = data['rnps'].lower() in source.data['rnps'].lower() if 'rnps' in source.data else False
    year_start = data['year_start'].lower() in source.data['year_start'].lower() if 'year_start' in source.data else False
    year_end = data['year_end'].lower() in source.data['year_end'].lower() if 'year_end' in source.data else False

    if and_op:
        return title and description and url and issn and rnps and year_start and year_end
    else: 
        return title or description or url or issn or rnps or year_start or year_end


@api_blueprint.route('/sources/count')
def get_sources_count():
    """retorna la cantidad de sources"""
    result = Sources.query.count()
    return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok','count', result) 

@api_blueprint.route('/source/id/<id>')
def get_source_by_id(id):    
    src = Sources.query.filter_by(id=id)
    return jsonify_source(src)

@api_blueprint.route('/source/uuid/<uuid>')
def get_source_by_uuid(uuid):    
    src = Sources.query.filter_by(uuid=uuid)
    return jsonify_source(src)

def jsonify_source(src):
    if src:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','sources', \
                            sources_schema_full.dump(src).data)
    return iroko_json_response(IrokoResponseStatus.ERROR, 'Sources not found', None, None)

def load_term_children_id(term):    
    if term.children:
        children = []
        for child in term.children:
            children.append(child.id)
            load_term_children_id(child)
        return children

def load_terms_tree(terms):
    children = []
    for par_term in terms:
        if str(par_term).isdigit():
            aux = Term.query.filter_by(id=par_term).first()        
            tchildren = load_term_children_id(aux)
            if tchildren:
                children += tchildren
    return set(children + terms)
