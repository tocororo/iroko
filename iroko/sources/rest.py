"""Iroko sources api views."""

from __future__ import absolute_import, print_function

import datetime
import traceback

from flask import Blueprint, request
from flask_babelex import lazy_gettext as _
from flask_login import current_user
from flask_principal import PermissionDenied
from invenio_oauth2server import require_api_auth

from iroko.notifications.api import Notifications
from iroko.notifications.marshmallow import NotificationSchema
from iroko.notifications.models import NotificationType
from iroko.sources.api import (
    SourceRecord, IrokoSourceVersions,
)
from iroko.sources.marshmallow.source import (
    source_version_schema, source_version_schema_many,
)
from iroko.sources.marshmallow.source_v1 import source_data_schema_many
from iroko.sources.models import SourceStatus
from iroko.utils import iroko_json_response, IrokoResponseStatus

api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
    url_prefix='/source'
)


@api_blueprint.route('/get', methods=['GET'])
def get_source_by_uuid_no_versions():
    """Get a source by any PID received as a argument, including UUID"""
    try:
        pid = request.args.get('pid')
        source = SourceRecord.get_source_by_pid(pid)
        if not source:
            raise Exception('Source not found')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                   'ok', 'source', \
                                   {'data': source})
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/new', methods=['POST'])
@require_api_auth()
def source_new():
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json

        user_id = current_user.id
        msg, source = SourceRecord.new_source(input_data, user_id=user_id)
        if not source:
            raise Exception(msg)

        notification = NotificationSchema()
        notification.classification = NotificationType.INFO
        notification.description = _(
            'Nueva fuente ingresada, requiere revisión de un gestor {0} ({1})'.format(source, source.id))
        notification.emiter = _('Sistema')

        for user_id in source.get_managers:
            notification.receiver_id = user_id
            Notifications.new_notification(notification)

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                   'ok', 'source', \
                                   {'data': source, 'count': 1})

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/<uuid>/versions', methods=['GET'])
@require_api_auth()
def get_source_by_uuid(uuid):
    """Get all source versions by source UUID, with permission checking"""

    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Source not found')

        with source.current_user_has_edit_permission.require():
            versions = IrokoSourceVersions.get_versions(uuid)
            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                       'ok', 'versions', \
                                       source_version_schema_many.dump(versions))
    except Exception as e:
        print()
        return iroko_json_response(IrokoResponseStatus.ERROR, traceback.format_exc(), None, None)


@api_blueprint.route('/<uuid>/edit', methods=['POST'])
@require_api_auth()
def source_new_version(uuid):
    # inserta un nuevo sourceVersion de un source que ya existe
    # input_data = request.json
    # source = Sources.get_source_by_id(uuid=uuid)
    # Sources.insert_new_source_version(input_data, source, False)

    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json
        user_id = current_user.id

        comment = 'no comment'
        if 'comment' in input_data:
            comment = input_data['comment']

        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')

        with source.current_user_has_edit_permission.require():
            # si no esta aprobada significa que siempre es la current.
            # si esta aprobada el proceso es otro
            print(input_data)
            is_current = source.status != SourceStatus.APPROVED.value
            source_version = IrokoSourceVersions.new_version(source.id,
                                                             input_data,
                                                             user_id=user_id,
                                                             comment=comment,
                                                             is_current=is_current)
            if not source_version:
                raise Exception('Not source for changing found')

            notification = NotificationSchema()
            notification.classification = NotificationType.INFO
            notification.description = _('Editor has change this source: {0}.'.format(source.name))
            notification.emiter = _('Sistema')

            for user in source.get_managers:
                notification.receiver_id = user
                Notifications.new_notification(notification)

            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'source_version',
                                       source_version_schema.dump(source_version))
    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/<uuid>/publish/<version>', methods=['POST'])
@require_api_auth()
def source_publish(uuid, version):
    # pone los datos de source_version en el sourceRecord
    # ademas source_status = SourceStatus.APPROVED
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')

        source_version = IrokoSourceVersions.get_version(version)
        if not source_version:
            raise Exception('Not source version found')

        with source.current_user_has_publish_permission.require():
            data = source_version.data
            data['source_status'] = SourceStatus.APPROVED.value
            source.update(data)

            notification = NotificationSchema()
            notification.classification = NotificationType.INFO
            notification.description = _('Se ha publicado una nueva version de la fuente: {0}.'.format(source.name))
            notification.emiter = _('Sistema')

            for user in source.get_managers:
                notification.receiver_id = user
                Notifications.new_notification(notification)

            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'source',
                                       source)
    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/<uuid>/unpublish', methods=['POST'])
@require_api_auth()
def source_unpublish(uuid):
    # pone source_status = SourceStatus.TO_REVIEW
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')

        with source.current_user_has_publish_permission.require():
            source.model.json['source_status'] = SourceStatus.TO_REVIEW.value
            source.commit()

            notification = NotificationSchema()
            notification.classification = NotificationType.INFO
            notification.description = _('Se ha despublicado la fuente: {0}.'.format(source.name))
            notification.emiter = _('Sistema')

            for user in source.get_managers:
                notification.receiver_id = user
                Notifications.new_notification(notification)

            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'source',
                                       source)
    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/me/<role>/<status>')
@require_api_auth()
def get_sources_from_user_as_manager(role, status):
    """
        returns the sources of wich current_user is manager
        param status: 'ALL', 'APPROVED', 'TO_REVIEW', 'UNOFFICIAL'
    """

    print("## start get sources {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))
    try:
        count = int(request.args.get('size')) if request.args.get('size') else 10
        page = int(request.args.get('page')) if request.args.get('page') else 1

        if page < 1:
            page = 1
        offset = count * (page - 1)
        limit = offset + count
        print(offset)
        print(limit)
        print(status)
        if status == 'ALL':
            status = None
        if role == 'manager':
            search = SourceRecord.get_sources_search_of_user_as_manager(current_user, status=status)
        elif role == 'editor':
            search = SourceRecord.get_sources_search_of_user_as_editor(current_user, status=status)
        else:
            raise Exception("role should be manager or editor")

        response = iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            'ok',
            'sources',
            {'total': search.count(), 'hits': source_data_schema_many.dump(search[offset:limit].execute())}
        )
        print("## iroko_json_response {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))
        return response

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)



@api_blueprint.route('/editor/<uuid>/versions', methods=['GET'])
@require_api_auth()
def get_editor_source_versions(uuid):
    try:
        # listar las versiones de este editor que no se han revisado para que pueda cambiarlas
        source = SourceRecord.get_record(uuid)
        print('source> ', source)
        if not source:
            raise Exception('Not source found')

        with source.current_user_has_edit_permission.require():
            versions = source.get_editor_versions_not_reviewed()
            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                       'ok', 'source', \
                                       {
                                           'data':     source,
                                           'versions': source_version_schema_many.dump(versions),
                                           'count':    1
                                       })

    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)

