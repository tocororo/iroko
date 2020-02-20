"""Iroko sources api views."""

from __future__ import absolute_import, print_function
from flask_babelex import lazy_gettext as _
from flask import Blueprint, current_app, jsonify, request, json, render_template, flash, url_for, redirect
from flask_login import login_required
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.sources.marshmallow import source_schema, source_schema_many, source_schema_no_versions, source_version_schema, source_version_schema_many
from iroko.sources.models import Source, SourceVersion, SourceType, SourceStatus
from marshmallow import ValidationError
from iroko.sources.api import Sources, get_current_user_source_permissions
from invenio_i18n.selectors import get_locale
from invenio_oauth2server import require_api_auth
from iroko.decorators import source_admin_required
from flask_principal import PermissionDenied
from iroko.sources.permissions import source_term_gestor_permission_factory, source_editor_permission_factory, source_gestor_permission_factory, user_has_editor_or_gestor_permissions
from iroko.notifications.marshmallow import NotificationSchema
from iroko.notifications.api import Notifications
from iroko.notifications.models import NotificationType



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
def get_source_by_uuid_no_versions(uuid):
    """Get a source by UUID"""
    try:
        source = Sources.get_source_by_id(uuid=uuid)
        if not source:
            raise Exception('Source not found')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','source', \
                            source_schema_no_versions.dump(source))

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/<uuid>/versions')
@require_api_auth()
def get_source_by_uuid(uuid):
    """Get a source and its versions by UUID, with permission checking"""
    try:
        source = Sources.get_source_by_id(uuid=uuid)
        if not source:
                raise Exception('Source not found')

        terms = ''
        for term in source.terms:
            terms = terms + str(term.term.uuid) + ','
        if terms:
            terms = terms[0:-1]

        if user_has_editor_or_gestor_permissions({'terms': terms, 'uuid':uuid}):

            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                'ok','source', \
                                source_schema.dump(source))

        raise PermissionDenied('No tiene permiso')

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

        notification = NotificationSchema()
        notification.classification = NotificationType.INFO
        notification.description = _('Nueva fuente ingresada, requiere revisión de un gestor {0}'.format(source.name))
        notification.emiter = _('Sistema')

        msg, users = Sources.get_user_ids_source_gestor(source.uuid)
        if users:
            for user_id in users:
                notification.receiver_id = user_id
                Notifications.new_notification(notification)


        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','source', \
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
            terms = terms + str(term.term.uuid) + ','
        if terms:
            terms = terms[0:-1]

        try:
            with source_editor_permission_factory({'uuid':uuid}).require():
                # si no esta aprobada significa que siempre es la current.
                # si esta aprobada el proceso es otro
                is_current = source.source_status is not SourceStatus.APPROVED
                msg, source, source_version = Sources.insert_new_source_version(input_data, uuid, is_current)
                if not source or not source_version:
                    raise Exception('Not source for changing found')

                notification = NotificationSchema()
                notification.classification = NotificationType.INFO
                notification.description = _('Editor has change this source: {0}.'.format(source.name))
                notification.emiter = _('Sistema')

                msg, users = Sources.get_user_ids_source_gestor(source.uuid)
                if users:
                    for user_id in users:
                        notification.receiver_id = user_id
                        Notifications.new_notification(notification)

                return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','sources', \
                            {'data': source_schema.dump(source), 'count': 1})
        except PermissionDenied as e:
            with source_term_gestor_permission_factory({'terms': terms, 'uuid':uuid}).require():
                msg, source, source_version = Sources.insert_new_source_version(input_data, uuid, True)
                if not source or not source_version:
                    raise Exception('Not source for changing found')

                notification = NotificationSchema()
                notification.classification = NotificationType.INFO
                notification.description = _('Gestor has reviewed this soruce: {0}.'.format(source.name))
                notification.emiter = _('Sistema')

                msg, users = Sources.get_user_ids_source_editor(source.uuid)
                if users:
                    for user_id in users:
                        notification.receiver_id = user_id
                        Notifications.new_notification(notification)

                return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                            'ok','source', \
                            {'data': source_schema.dump(source), 'count': 1})

    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/<id>/version/edit', methods=['POST'])
@require_api_auth()
def source_edit_version(id):
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json

        version = Sources.get_source_version_by_id(id)
        if not version:
            raise Exception('Not version found')

        source = Sources.get_source_by_id(uuid=version.source.uuid)

        if not source:
            raise Exception('Not source found')

        with source_editor_permission_factory({'uuid':source.uuid}).require():
            msg, source, source_version = Sources.edit_source_version(input_data, version)
            if not source or not source_version:
                raise Exception('Not source for changing found')

            notification = NotificationSchema()
            notification.classification = NotificationType.INFO
            notification.description = _('The edit has change data in version of source: {0}.'.format(source.name))
            notification.emiter = _('System')

            msg, users = Sources.get_user_ids_source_gestor(source.uuid)
            if users:
                for user_id in users:
                    notification.receiver_id = user_id
                    Notifications.new_notification(notification)

            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','source', \
                        {
                            'data': source_schema_no_versions.dump(source),
                            'version': source_version_schema.dump(source_version),
                            'count': 1
                        })

    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
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
            terms = terms + str(term.term.uuid) + ','
        if terms:
            terms = terms[0:-1]

        with source_term_gestor_permission_factory({'terms': terms, 'uuid':uuid}).require():
            msg, source  = Sources.set_source_current(input_data, source)
            if not source:
                raise Exception('Not source for changing found')

            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','source', \
                        {'data': source_schema.dump(source), 'count': 1})

    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
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

            notification = NotificationSchema()
            notification.classification = NotificationType.INFO
            notification.description = _('El gestor ha aprobado para incluir en Sceiba la fuente: {0}.'.format(source.name))
            notification.emiter = _('Sistema')

            msg, users = Sources.get_user_ids_source_editor(source.uuid)
            if users:
                for user_id in users:
                    notification.receiver_id = user_id
                    Notifications.new_notification(notification)

            return iroko_json_response(
                IrokoResponseStatus.SUCCESS,
                'Source {0} approved.'.format(source.name),
                'source',
                source_schema.dump(source)
            )

    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
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
        param status: 'all', 'approved', 'to_review', 'unofficial'
    """
    try:
        count = int(request.args.get('count')) if request.args.get('count') else 9
        page = int(request.args.get('page')) if request.args.get('page') else 0

        limit = count
        offset = count*page

        msg, sources  = Sources.get_sources_from_editor_current_user(status)
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'sources',
            source_schema_many.dump(sources[offset:offset+limit])
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/gestor/sources/<status>')
@require_api_auth()
def get_sources_from_gestor(status):
    """
        param status: 'all', 'approved', 'to_review', 'unofficial'
    """
    try:
        count = int(request.args.get('count')) if request.args.get('count') else 9
        page = int(request.args.get('page')) if request.args.get('page') else 0

        limit = count
        offset = count*page

        msg, sources  = Sources.get_sources_from_gestor_current_user(status)

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'sources',
            source_schema_many.dump(sources[offset:offset+limit])
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/me/sources/<status>')
@require_api_auth()
def get_sources_from_user(status):
    """
        param status: 'all', 'approved', 'to_review', 'unofficial'
    """
    try:
        count = int(request.args.get('count')) if request.args.get('count') else 9
        page = int(request.args.get('page')) if request.args.get('page') else 0

        limit = count
        offset = count*page

        msg, sources_gestor  = Sources.get_sources_from_gestor_current_user(status)
        msg, sources_editor  = Sources.get_sources_from_editor_current_user(status)

        in_first = set(sources_gestor)
        in_second = set(sources_editor)

        in_second_but_not_in_first = in_second - in_first

        result = sources_gestor + list(in_second_but_not_in_first)

        # TODO: optimizar esta operacion porque puede ser lenta
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            msg,
            'sources',
            source_schema_many.dump(result[offset:offset+limit])
            )

    except Exception as e:
        msg = str(e)

    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/editor/<uuid>/versions', methods=['GET'])
@require_api_auth()
def get_editor_source_versions(uuid):
    try:
        #listar las versiones de este editor que no se han revisado para que pueda cambiarlas
        source = Sources.get_source_by_id(uuid=uuid)
        print('source> ', source)
        if not source:
            raise Exception('Not source found')

        with source_editor_permission_factory({'uuid':source.uuid}).require():
            versions = Sources.get_editor_versions_not_reviewed(source)
            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','source', \
                        {
                            'data': source_schema.dump(source),
                            'versions':source_version_schema_many.dump(versions),
                            'count': 1
                        })

    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
