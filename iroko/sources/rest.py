"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, jsonify, request, json, render_template, flash, url_for, redirect
from flask_login import login_required
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.sources.marshmallow import source_schema, source_schema_many
from iroko.sources.models import Source, SourceVersion, SourceType, SourceStatus
from marshmallow import ValidationError
from iroko.sources.api import Sources, get_current_user_source_permissions
from invenio_i18n.selectors import get_locale
from invenio_oauth2server import require_api_auth
from iroko.decorators import source_admin_required
from flask_principal import PermissionDenied
from iroko.sources.permissions import source_term_gestor_permission_factory, source_editor_permission_factory, source_gestor_permission_factory



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


# @api_blueprint.route('/<uuid>')
# def get_source_version_by_uuid(uuid):
#     """Get a source version by UUID of the source"""
#     try: 
#         source = Sources.get_source_by_id(uuid=uuid)
#         if not source:
#             raise Exception('Source not found')

#         return iroko_json_response(IrokoResponseStatus.SUCCESS, \
#                         'ok','sources', \
#                         {'data': source_schema.dump(source), 'count': 1})

#     except Exception as e:
#         return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)   


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

@api_blueprint.route('/<uuid>/edit', methods=['POST'])
@require_api_auth()
def source_new_version(uuid):

    # inserta un nuevo sourceVersion de un source que ya existe
    # hay que comprobar que el usuario que inserta, es quien creo el source (el que tiene el sourceversion mas antiguo) o un usuario con el role para crear cualquier tipo de versiones.
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json
        
        source = Sources.get_source_by_id(uuid=uuid)

        if not source:
            raise Exception('Not source found')
        
        terms = ''
        for term in source.terms:
            terms = terms + str(term.id) + ','
        if terms:
            terms = terms[1,-1]

        try:
            with source_editor_permission_factory({'uuid':uuid}).require():
                is_current = source.source_status is not SourceStatus.APPROVED 
                msg, source, source_version = Sources.insert_new_source_version(input_data, uuid, is_current)
                if not source or not source_version:                
                    raise Exception('Not source for changing found')

                return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','sources', \
                            {'data': source_schema.dump(source), 'count': 1})
        except PermissionDenied as e:
            with source_term_gestor_permission_factory({'terms': terms, 'uuid':uuid}).require():                
                msg, source, source_version = Sources.insert_new_source_version(input_data, uuid, True)
                if not source or not source_version:                
                    raise Exception('Not source for changing found')

                return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','sources', \
                            {'data': source_schema.dump(source), 'count': 1})

    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)   


@api_blueprint.route('/<uuid>/current', methods=['POST'])
@require_api_auth()
def source_version_set_current(uuid):
    # pone un sourceVersion como current version en source y recibe tambien el estatus para el source
    # comprobar que el usuario tiene el role para hacer esto.
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json
        
        source = Sources.get_source_by_id(uuid=uuid)

        if not source:
            raise Exception('Not source found')
        
        terms = ''
        for term in source.terms:
            terms = terms + str(term.id) + ','
        if terms:
            terms = terms[1,-1]

        with source_term_gestor_permission_factory({'terms': terms, 'uuid':uuid}).require():
            msg, source  = Sources.set_source_current(input_data, source)
            if not source:                
                raise Exception('Not source for changing found')

            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema.dump(source), 'count': 1})

    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)   


@api_blueprint.route('/<uuid>/approved', methods=['GET', 'POST'])
@require_api_auth()
def source_set_approved(uuid):    
    try:
        source = Sources.get_source_by_id(uuid=uuid)
        if not source:
            raise Exception('Source not found.')
        
        with source_gestor_permission_factory({'uuid': uuid}).require():
            Sources.set_source_approved(source)
            return iroko_json_response(
                IrokoResponseStatus.SUCCESS,
                'Source {0} approved.'.format(source.name),
                'approved',
                source_schema.dumps(source)
            )
    
    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/user/permissions')
@require_api_auth()
def sources_current_user_permissions():
    msg = ''
    try:
        actions, vocabs  = get_current_user_source_permissions()
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'permissions',
            {actions:vocabs}
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/gestor/<uuid>')
@require_api_auth()
def get_source_gestor(uuid):
    
    try:
        msg, user_ids  = Sources.get_user_ids_source_gestor(uuid)
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'users',
            user_ids
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/editor/sources/<status>')
@require_api_auth()
def get_sources_from_editor(status):
    """
        param status: 'all', 'approved', 'review', 'unofficial'
    """
    try:
        msg, sources  = Sources.get_sources_from_editor_current_user(status)
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'sources',
            source_schema_many.dumps(sources)
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/gestor/sources/<status>')
@require_api_auth()
def get_sources_from_gestor(status):
    """
        param status: 'all', 'approved', 'review', 'unofficial'
    """        
    try:
        msg, sources  = Sources.get_sources_from_gestor_current_user(status)
        
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'sources',
            source_schema_many.dumps(sources)
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/me/sources/<status>')
@require_api_auth()
def get_sources_from_user(status):
    """
        param status: 'all', 'approved', 'review', 'unofficial'
    """        
    try:
        msg, sources_gestor  = Sources.get_sources_from_gestor_current_user(status)
        msg, sources_editor  = Sources.get_sources_from_editor_current_user(status)        
        
        in_first = set(sources_gestor)
        in_second = set(sources_editor)

        in_second_but_not_in_first = in_second - in_first

        result = sources_gestor + list(in_second_but_not_in_first)
        print(result)

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'sources',
            source_schema_many.dumps(result)
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


