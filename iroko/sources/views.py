
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json, render_template

from iroko.utils import iroko_json_response, IrokoResponseStatus

from iroko.sources.marshmallow import sources_schema_full

from iroko.sources.api import Sources

blueprint = Blueprint(
    'iroko_sources',
    __name__,
    template_folder='templates',
    static_folder='static',
)

@blueprint.route('/source/<id>')
def view_source_id(id):
    src = Sources.get_source_by_id(id=id)
    source = source_schema_full.dump(src)
    return render_template('source.html', source=source.data)


api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
)

@api_blueprint.route('/sources')
def get_sources():

    and_op = True if request.args.get('op') and request.args.get('op') == 'and' else False

    count = int(request.args.get('count')) if request.args.get('count') else 10
    page = int(request.args.get('page')) if request.args.get('page') else 0

    limit = count
    offset = count*page

    tids = request.args.get('terms')
    terms = []
    if tids:
        tids= tids.split(',')
        term_op = tids[0]    
        if tids[0].lower() == 'and' or tids[0].lower() == 'or':
            del tids[0]    
        terms = tids

    repo_args = {
        'harvest_type' : str(request.args.get('harvest_type')),
        'has_harvest_endpoint': str(request.args.get('has_harvest_endpoint')),
        'harvest_status': str(request.args.get('harvest_status'))
    }
    data_args = {
        'title' : str(request.args.get('title')),
        'description': str(request.args.get('description')),
        'url': str(request.args.get('url')),
        'issn': str(request.args.get('issn')),
        'rnps': str(request.args.get('rnps')),
        'year_start': str(request.args.get('year_start')),
        'year_end': str(request.args.get('year_end'))
    }

    result = Sources.get_sources(and_op, terms, data_args, repo_args)
    if result:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': sources_schema_full.dump(result[offset:offset+limit]).data,\
                         'count': len(result)})
    return iroko_json_response(IrokoResponseStatus.ERROR, 'Sources not found', None, None)


@api_blueprint.route('/sources/count')
def get_sources_count():
    """retorna la cantidad de sources"""
    result = Sources.count_sources()
    return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok','count', result) 

@api_blueprint.route('/source/id/<id>')
def get_source_by_id(id):    
    src = Sources.get_source_by_id(id=id)
    return jsonify_source(src)

@api_blueprint.route('/source/uuid/<uuid>')
def get_source_by_uuid(uuid):    
    src = Sources.get_source_by_id(uuid=uuid)
    return jsonify_source(src)

def jsonify_source(src):
    if src:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','sources', \
                            {'data': sources_schema_full.dump(src).data,\
                             'count': 1})
    return iroko_json_response(IrokoResponseStatus.ERROR, 'Sources not found', None, None)



