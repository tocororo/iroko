
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, jsonify, request, json, render_template, flash, url_for, redirect
from flask_login import login_required
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.sources.marshmallow import source_schema
from iroko.sources.models import Source, SourceVersion, SourceType, SourceStatus
from marshmallow import ValidationError
from iroko.sources.api import Sources
from invenio_i18n.selectors import get_locale
from invenio_oauth2server import require_api_auth
from iroko.decorators import source_admin_required
from iroko.sources.permissions import source_editor_permission_factory, source_gestor_permission_factory, source_admin_permission_factory



api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
    url_prefix='/source'
)


@api_blueprint.route('/count')
def get_sources_count():
    """return sources count"""

    try:
        result = Sources.count_sources()
        if not result:
            raise Exception('Sources not found')
        
        return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok','count', result)
        
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)    


@api_blueprint.route('/<uuid>')
def get_source_by_uuid(uuid):
    """Get a source by UUID"""
    try: 
        source = Sources.get_source_by_id(uuid=uuid)
        if not source:
            raise Exception('Source not found')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema.dump(source), 'count': 1})

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)   


@api_blueprint.route('/new', methods=['POST'])
@require_api_auth()
def source_new():
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json

        msg, source = Sources.insert_new_source(input_data)
        if not source:
            raise Exception(msg)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema.dump(source), 'count': 1})
                            
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)   



    # Crear un Source y un SourceVersion que tienen el mismo Data.
    # comprobar que no exista otro ISSN, RNPS o URL igual, sino da error
    # source_status = REview
    # supuestamente en source.data.terms vienen los terminos relacionados y eso hay que reflejarlo en la tabla TermSources
    # Aqui no se trata la parte que tiene en ver con repo!!!!

@api_blueprint.route('/<uuid>/new-version', methods=['POST'])
@require_api_auth()
def source_new_version(uuid):

    # inserta un nuevo sourceVersion de un source que ya existe
    # hay que comprobar que el usuario que inserta, es quien creo el source (el que tiene el sourceversion mas antiguo) o un usuario con el role para crear cualquier tipo de versiones.
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json

        with source_admin_permission_factory({'uuid': uuid}).require():
            is_current = True if "is_current" in input_data else False

            msg, source, source_version = Sources.insert_new_source_version(input_data, uuid, is_current)
            if not source or not source_version:                
                raise Exception('Not source for changing found')

            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema.dump(source), 'count': 1})
    
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)   


@api_blueprint.route('/<uuid>/current', methods=['GET', 'POST'])
@require_api_auth()
def source_version_set_current(uuid):
    # pone un sourceVersion como current version en source y recibe tambien el estatus para el source
    # comprobar que el usuario tiene el role para hacer esto.
    try:
        with source_gestor_permission_factory({'uuid': uuid}).require():
            src = Sources.get_source_by_id(uuid=uuid)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)

