
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



api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
)


@api_blueprint.route('/sources/count')
def get_sources_count():
    """return sources count"""

    result = Sources.count_sources()
    return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok','count', result)


@api_blueprint.route('/source/<uuid>')
def get_source_by_uuid(uuid):
    """Get a source by UUID"""

    source = Sources.get_source_by_id(uuid=uuid)
    if source:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema.dump(source), 'count': 1})
    return iroko_json_response(IrokoResponseStatus.NOT_FOUND, 'Sources not found', None, None)


#TODO: Need authentication
@api_blueprint.route('/source/new', methods=['POST'])
def source_new():

    # FIXME: get current user!!!!
    user = None
    if not request.is_json:
        return {"message": "No JSON data provided"}, 400
    input_data = request.json

    msg, source = Sources.insert_new_source(user, input_data)

    if source:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema.dump(source), 'count': 1})
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)



    # Crear un Source y un SourceVersion que tienen el mismo Data.
    # comprobar que no exista otro ISSN, RNPS o URL igual, sino da error
    # source_status = REview
    # supuestamente en source.data.terms vienen los terminos relacionados y eso hay que reflejarlo en la tabla TermSources
    # Aqui no se trata la parte que tiene en ver con repo!!!!



#TODO: Need authentication
@api_blueprint.route('/source/<uuid>/new-version', methods=['POST'])
def source_new_version(uuid):

    # inserta un nuevo sourceVersion de un source que ya existe
    # hay que comprobar que el usuario que inserta, es quien creo el source (el que tiene el sourceversion mas antiguo) o un usuario con el role para crear cualquier tipo de versiones.
    # FIXME: get current user!!!!
    user = None

    if not request.is_json:
        return {"message": "No input data provided"}, 400

    input_data = request.json

    # FIXME: Check if user have permission to do this, if not, just add the version!!!
    is_current = True if "is_current" in input_data else False

    msg, source_version = Sources.insert_new_source_version(user, json_data, uuid, is_current)
    if source_version:
        source = Source.query.filter_by(uuid=source_uuid).first()
        if source:
            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema.dump(source), 'count': 1})
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)




#TODO: Necesita autenticacion.
@api_blueprint.route('/source/<id>/current', methods=['GET', 'POST'])
def source_version_set_current(id):

    # pone un sourceVersion como current version en source y recibe tambien el estatus para el source
    # comprobar que el usuario tiene el role para hacer esto.

    src = Sources.get_source_by_id(id=id)



