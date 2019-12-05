
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, jsonify, request, json, render_template, flash, url_for, redirect
from flask_login import login_required
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.sources.marshmallow import source_schema_full_many_no_versions, source_schema_full, source_data_schema
from iroko.sources.models import Source, SourceVersion, SourceType, SourceStatus
from marshmallow import ValidationError
from iroko.sources.api import Sources
from invenio_i18n.selectors import get_locale
from .forms import InclusionForm
from flask_babelex import lazy_gettext as _
import json
#from iroko.utils import mail
from flask_mail import Message
import unicodedata
import re
import random
from datetime import datetime


blueprint = Blueprint(
    'iroko_sources',
    __name__,
    url_prefix='/iroko-sources',
    template_folder='templates',
    static_folder='static',
)


api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
)


@api_blueprint.route('/sources')
def get_sources():
    """List all sources with filters in parameters"""
    # TODO: document this!!!

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
    if result is not None:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema_full_many_no_versions.dump(result[offset:offset+limit]).data,\
                         'count': len(result)})
    return iroko_json_response(IrokoResponseStatus.NOT_FOUND, 'Sources not found', None, {'count': 0})


@api_blueprint.route('/sources/count')
def get_sources_count():
    """return sources count"""

    result = Sources.count_sources()
    return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok','count', result)


@api_blueprint.route('/source/id/<id>')
def get_source_by_id(id):
    """Get a source by ID"""

    src = Sources.get_source_by_id(id=id)
    print(src.data)
    return jsonify_source(src)


@api_blueprint.route('/source/uuid/<uuid>')
def get_source_by_uuid(uuid):
    """Get a source by UUID"""

    src = Sources.get_source_by_id(uuid=uuid)
    return jsonify_source(src)


#TODO: Need authentication
@api_blueprint.route('/source/new', methods=['POST'])
def source_new():

    # FIXME: get current user!!!!
    user = None

    if not request.is_json:
        return {"message": "No input data provided"}, 400

    input_data = request.json

    try:
        source_type = SourceType(input_data["type"])
        try:
            data = source_data_schema.loads(input_data["data"])
        except ValidationError as err:
            return err.messages, 422
        else:
            msg, source = Sources.insert_new_source(user, input_data, source_type)
            return {"message": msg}, 201
    except Exception as exc:
        return {"message": "Not source type provided"}, 412


    # Crear un Source y un SourceVersion que tienen el mismo Data.
    # comprobar que no exista otro ISSN, RNPS o URL igual, sino da error
    # source_status = REview
    # supuestamente en source.data.terms vienen los terminos relacionados y eso hay que reflejarlo en la tabla TermSources
    # Aqui no se trata la parte que tiene en ver con repo!!!!



#TODO: Need authentication
@api_blueprint.route('/source/<id>/new-version', methods=['GET', 'POST'])
def source_new_version(id):

    # inserta un nuevo sourceVersion de un source que ya existe
    # hay que comprobar que el usuario que inserta, es quien creo el source (el que tiene el sourceversion mas antiguo) o un usuario con el role para crear cualquier tipo de versiones.
    # FIXME: get current user!!!!
    user = None

    if not request.is_json:
        return {"message": "No input data provided"}, 400

    input_data = request.json

    # FIXME: Check if user have permission to do this, if not, just add the version!!!
    is_current = True if "is_current" in input_data else False

    Sources.insert_new_source_version(user, json_data, id, is_current)

    try:
        source_type = SourceType(input_data["type"])
        try:
            data = source_data_schema.loads(input_data["data"])
        except ValidationError as err:
            return err.messages, 422
        else:
            msg, source = Sources.insert_new_source(user, input_data, source_type)
            return {"message": msg}, 201
    except Exception as exc:
        return {"message": "Not source type provided"}, 412



#TODO: Necesita autenticacion.
@api_blueprint.route('/source/<id>/current', methods=['GET', 'POST'])
def source_version_set_current(id):

    # pone un sourceVersion como current version en source y recibe tambien el estatus para el source
    # comprobar que el usuario tiene el role para hacer esto.

    src = Sources.get_source_by_id(id=id)



def jsonify_source(src):
    if src:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','sources', \
                            {'data': source_schema_full.dump(src), 'count': 1})
    return iroko_json_response(IrokoResponseStatus.NOT_FOUND, 'Sources not found', None, None)

