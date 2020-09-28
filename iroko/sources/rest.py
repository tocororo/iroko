"""Iroko sources api views."""

from __future__ import absolute_import, print_function

import datetime
import traceback

from elasticsearch_dsl import A
from flask import Blueprint, request
from flask_babelex import lazy_gettext as _
from flask_login import current_user
from flask_principal import PermissionDenied
from invenio_access import ActionUsers
from invenio_accounts.models import User
from invenio_db import db
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
from iroko.sources.marshmallow.source_v1 import source_v1_response
from iroko.sources.models import SourceStatus
from iroko.sources.permissions import is_user_souces_admin, ObjectSourceOrganizationManager, ObjectSourceTermManager
from iroko.sources.search import SourceSearch
from iroko.userprofiles import UserProfile
from iroko.utils import iroko_json_response, IrokoResponseStatus

api_blueprint = Blueprint(
    'iroko_api_sources',
    __name__,
    url_prefix='/source'
)


@api_blueprint.route('/new', methods=['POST'])
@require_api_auth()
def source_new():
    """
    Create a new Source,
    If is a regular user, then the user will be Source Editor, but sceiba
    arguments:
        pid: must provide a source PID to create something.
        role: user role in the source.
    :return:
    """
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json

        user_id = current_user.id

        pidvalue = request.args.get('pid')
        role = request.args.get('role')

        comment = 'New Inclusion'
        if 'comment' in input_data:
            comment = input_data['comment']

        data = dict(input_data['data'])
        print(data)
        pid, source = SourceRecord.get_source_by_pid(pidvalue)
        if not source or not pid:
            pid, source = SourceRecord.get_source_by_pid_in_data(data)
        if source:
            print(source)
            msg, done = source.grant_source_editor_permission(user_id)
            UserProfile.add_source_to_user_profile(user_id, source['id'], role)
            if done:
                source_version = IrokoSourceVersions.new_version(source.id,
                                                             data,
                                                             user_id=user_id,
                                                             comment=comment,
                                                             is_current=False)

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
            data = dict(input_data['data'])
            source_version = IrokoSourceVersions.new_version(source.id,
                                                             data,
                                                             user_id=user_id,
                                                             comment=comment,
                                                             is_current=False)
            if not source_version:
                raise Exception('Not source for changing found')

            notification = NotificationSchema()
            notification.classification = NotificationType.INFO
            notification.description = _('Editor has change this source: {0}.'.format(source['name']))
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
        raise e
        # return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/byissn/<issn>')
def get_source_by_issn(issn):
    """Get a source by any PID received as a argument, including UUID"""

    print('eres la api correcta?')
    print('eres la api correcta?')
    try:
        print('eres la api correcta?')
        pid, source = SourceRecord.create_or_get_source_by_issn(issn)
        if not source or not pid:
            raise Exception('Source not found')

        return source_v1_response(pid, source)

        # return iroko_json_response(IrokoResponseStatus.SUCCESS, \
        #                            'ok', 'source', \
        #                            {'data': source})
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/pid', methods=['GET'])
def get_source_by_pid():
    """Get a source by any PID received as a argument, including UUID"""
    try:
        pidvalue = request.args.get('value')
        pid, source = SourceRecord.get_source_by_pid(pidvalue)
        if not source or not pid:
            raise Exception('Source not found')

        return source_v1_response(pid, source)

        # return iroko_json_response(IrokoResponseStatus.SUCCESS, \
        #                            'ok', 'source', \
        #                            {'data': source})
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/<uuid>/versions', methods=['GET'])
@require_api_auth()
def get_source_versions(uuid):
    """Get all source versions by source UUID, with permission checking"""

    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Source not found')

        with source.current_user_has_edit_permission.require():
            versions = IrokoSourceVersions.get_versions(uuid)
            dd = source_version_schema_many.dump(versions)
            print(dd)
            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                       'ok', 'versions', \
                                       dd)
    except Exception as e:
        print()
        return iroko_json_response(IrokoResponseStatus.ERROR, traceback.format_exc(), None, None)


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


@api_blueprint.route('/me/<status>')
@require_api_auth()
def get_current_user_sources(status):
    """
        returns the sources of wich current_user is manager
        param status: 'ALL', 'APPROVED', 'TO_REVIEW', 'UNOFFICIAL'
    """

    print("## start get sources {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))
    try:
        # count = int(request.args.get('size')) if request.args.get('size') else 10
        # page = int(request.args.get('page')) if request.args.get('page') else 1
        #
        # if page < 1:
        #     page = 1
        # offset = count * (page - 1)
        # limit = offset + count
        # print(offset)
        # print(limit)
        print(status)
        if status == 'ALL':
            status = None
        # if role == 'manager':
        search = SourceRecord.get_sources_search_of_user_as_manager(current_user, status=status)
        manager = []
        if search is not None:
            # [offset: limit].execute()
            search_result = search.scan()
            # TODO: hay que buscar una manera de hacerlo por aqui
            # source_v1.serialize_search(
            #     iroko_source_uuid_fetcher, ss
            # )
            # por alguna razon esto no funciona,
            # la forma en que invenio lo hace incluye en los hits '_version', pero por defecto eso no esta.
            # print(search_result)
            # print(source_data_schema_many.dump(search_result))

            for hit in search_result:
                manager.append(
                    {
                        'id':                hit['id'],
                        'name':              hit['name'],
                        'source_status':     hit['source_status'],
                        'version_to_review': True
                    }
                )

        # elif role == 'editor':
        sources = SourceRecord.get_sources_search_of_user_as_editor(current_user, status=status)
        editor = []
        for hit in sources:
            editor.append(
                {
                    'id':                hit['id'],
                    'name':              hit['name'],
                    'source_status':     hit['source_status'],
                    'version_to_review': True
                }
            )

        response = iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            'ok',
            'sources',
            {'manager': manager, 'editor': editor}
        )

        # else:
        #     raise Exception("role should be manager or editor")

        # print("## iroko_json_response {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))
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


@api_blueprint.route('/aggs/org/<uuid>/', methods=['GET'])
def get_sources_by_organization_children(uuid):
    """
    Count all the sources from an organization, and count all the sources from the organization children
    :param uuid: the uuid of the organization
    :return:

    {
        'id': '<uuid>',
        'name': '<name>',
        'sources_count': '<count>'
        'children': [
            'id': '<uuid>',
            'name': '<name>',
            'sources_count': '<count>'
            'children': [
                ...
            ]
        ]
    }
    """

    # TODO:
    # 1- obtener de cuor, la organizacion con los hijos.
    # result = dict()
    # result['id'] = 'orgID'
    # 2- por cada uno de los hijos de la organizacion
    #  por ahora esta bien asi
    try:
        size = int(request.args.get('size')) if request.args.get('size') else 100
        size = size if size > 0 else 100

        search = SourceSearch()
        search = search.filter('term', organizations__id=uuid)
        # search.query = Q('match', **{'organizations.id': 'orgID'})
        a = A('terms', field='organizations.name', size=size)
        search.aggs.bucket('orgs', a)
        response = search.execute()
        result = []
        for item in response.aggregations.orgs.buckets:
            # item.key will the house number
            result.append({
                'key':       item.key,
                'doc_count': item.doc_count
            })
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                   'ok', 'source', \
                                   {
                                       'aggs': result,
                                   })
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


#
# @api_blueprint.route('/last/org/<uuid>/', methods=['GET'])
# def get_sources_by_organization_children(uuid):
#     """
#     get the last sources added from an organization.
#     :param uuid:
#     :return:
#     """
#     count = int(request.args.get('count')) if request.args.get('count') else 3
#     count = count if count > 0 else 3
#

@api_blueprint.route('/editor/<uuid>/<user>', methods=['POST'])
@require_api_auth()
def set_source_editor(uuid, user):
    """
    Set user as editor of a source
    :param uuid: source uuid
    :param user: user id
    :return:
    """
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')

        with source.current_user_has_publish_permission.require():
            msg, done = source.grant_source_editor_permission(user)
            if done:
                notification = NotificationSchema()
                notification.classification = NotificationType.INFO
                notification.description = _('Ha sido aprobado como editor de: {0}.'.format(source['title']))
                notification.emiter = _('Sistema')
                notification.receiver_id = user
                Notifications.new_notification(notification)

                return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                           'ok', 'permission',
                                           {
                                               'source':     uuid,
                                               'user':       user,
                                               'permission': 'editor'
                                           })
            raise Exception(msg)

    except PermissionDenied as err:
        msg = 'Permission denied'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/manager/<mtype>/<uuid>/<user>/', methods=['POST'])
@require_api_auth()
def set_source_manager(mtype, uuid, user):
    """
    Set user as manager of a organization
    :param mtype: type of manager, two possible values: org or term
    :param uuid: organization or term uuid
    :param user: user id
    :return:
    """
    try:
        if is_user_souces_admin(current_user):
            userObj = User.query.filter_by(id=user).first()
            if not userObj:
                raise Exception('User not found')
            else:
                with db.session.begin_nested():
                    if mtype == 'org':
                        db.session.add(ActionUsers.allow(ObjectSourceOrganizationManager(uuid), user=userObj))

                        notification = NotificationSchema()
                        notification.classification = NotificationType.INFO
                        notification.description = _(
                            'Ha sido aprobado como gestor de la Organizacion {0}.'.format(uuid))
                        notification.emiter = _('Sistema')
                        notification.receiver_id = user
                        Notifications.new_notification(notification)

                        return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                                   'ok', 'permission',
                                                   {
                                                       'org':        uuid,
                                                       'user':       user,
                                                       'permission': 'manager'
                                                   })
                    if mtype == 'term':
                        db.session.add(ActionUsers.allow(ObjectSourceTermManager(uuid), user=userObj))

                        notification = NotificationSchema()
                        notification.classification = NotificationType.INFO
                        notification.description = _(
                            'Ha sido aprobado como gestor del Termino {0}.'.format(uuid))
                        notification.emiter = _('Sistema')
                        notification.receiver_id = user
                        Notifications.new_notification(notification)

                        return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                                   'ok', 'permission',
                                                   {
                                                       'term':       uuid,
                                                       'user':       user,
                                                       'permission': 'manager'
                                                   })

        raise PermissionDenied()

    except PermissionDenied as err:
        msg = 'Permission denied'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
