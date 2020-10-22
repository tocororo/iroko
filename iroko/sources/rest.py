"""Iroko sources api views."""

from __future__ import absolute_import, print_function

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
from invenio_pidstore.errors import PIDObjectAlreadyAssigned

from iroko.notifications.api import Notifications
from iroko.notifications.marshmallow import NotificationSchema
from iroko.notifications.models import NotificationType
from iroko.sources.api import (
    SourceRecord, IrokoSourceVersions,
)
from iroko.sources.marshmallow.source import (
    source_version_schema, source_version_schema_many,
)
from iroko.sources.marshmallow.source_v1 import source_v1_response, source_v1
from iroko.sources.models import SourceStatus, SourceType
from iroko.sources.permissions import is_user_souces_admin, ObjectSourceOrganizationManager, ObjectSourceTermManager
from iroko.sources.search import SourceSearch
from iroko.userprofiles import UserProfile
from iroko.utils import iroko_json_response, IrokoResponseStatus, CuorHelper, IrokoVocabularyIdentifiers
from iroko.vocabularies.marshmallow import term_schema_many
from iroko.vocabularies.models import Term

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
        # TODO: Si ya esta publicado o si tiene mas de una version entoces se crea una version,
        data['source_status'] = SourceStatus.TO_REVIEW.value
        source = SourceRecord.new_source_revision(data, user_id, comment)

        # print(data)
        # pid, source = SourceRecord.get_source_by_pid(pidvalue)
        # if not source or not pid:
        #     pid, source = SourceRecord.get_source_by_pid_in_data(data)
        if source:
            # print(source)
            msg, done = source.grant_source_editor_permission(user_id)
            UserProfile.add_source_to_user_profile(user_id, source['id'], role)
            # if done:
            #     source_version = IrokoSourceVersions.new_version(source.id,
            #                                                  data,
            #                                                  user_id=user_id,
            #                                                  comment=comment,
            #                                                  is_current=False)

                # notification = NotificationSchema()
                # notification.classification = NotificationType.INFO
                # notification.description = _(
                #     'Nueva fuente ingresada, requiere revisión de un gestor {0} ({1})'.format(source, source.id))
                # notification.emiter = _('Sistema')
                #
                # for user_id in source.get_managers:
                #     notification.receiver_id = user_id
                #     Notifications.new_notification(notification)

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
            # print(input_data)

            # data = dict(input_data['data'])
            # data['source_status'] = SourceStatus.TO_REVIEW.value
            #
            # source.update(data)

            source_version = IrokoSourceVersions.new_version(source.id,
                                                             data,
                                                             user_id=user_id,
                                                             comment=comment,
                                                                 is_current=False)
            if not source_version:
                raise Exception('Not source for changing found')

            # notification = NotificationSchema()
            # notification.classification = NotificationType.INFO
            # notification.description = _('Editor has change this source: {0}.'.format(source['name']))
            # notification.emiter = _('Sistema')
            #
            # for user in source.get_managers:
            #     notification.receiver_id = user
            #     Notifications.new_notification(notification)

            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'source_version',
                                       source_version_schema.dump(source_version))
    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        raise e
        # return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/<uuid>/publish', methods=['POST'])
@require_api_auth()
def source_publish(uuid):
    # inserta un nuevo sourceVersion de un source que ya existe
    # input_data = request.json
    # updata el input_data en el SourceRecord

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

        with source.current_user_has_publish_permission.require():

            data = dict(input_data['data'])
            data['source_status'] = SourceStatus.APPROVED.value

            source.update(data)

            source_version = IrokoSourceVersions.new_version(source.id,
                                                             data,
                                                             user_id=user_id,
                                                             comment=comment,
                                                             is_current=True)

            if not source_version:
                raise Exception('Not source for changing found')



            # TODO: aqui hay un error con los get managers
            # notification = NotificationSchema()
            # notification.classification = NotificationType.INFO
            # notification.description = _('Se ha publicado una nueva version de la fuente: {0}:{1}.'.format(source['name'], source.id))
            # notification.emiter = _('Sistema')
            #
            # for user in source.get_managers:
            #     notification.receiver_id = user
            #     Notifications.new_notification(notification)

            # print('************************** to response')
            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'source',
                                       source)
    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
    except PIDObjectAlreadyAssigned as err:
        msg = 'El Identificador persistente ya existe: ' + str(err)
        # print('*******', msg)
    except Exception as e:
        msg = str(e)
    # print('*******', msg)
    return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)




@api_blueprint.route('/byissn/<issn>')
def get_source_by_issn(issn):
    """Get a source by any PID received as a argument, including UUID"""

    # print('eres la api correcta?')
    # print('eres la api correcta?')
    try:
        # print('eres la api correcta?')
        # pid, source = SourceRecord.create_or_get_source_by_issn(issn)
        pid, source = SourceRecord.get_source_by_pid(issn)
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

@api_blueprint.route('/<uuid>', methods=['GET'])
@require_api_auth()
def get_source_by_uuid_perm(uuid):
    """Get a source by any PID received as a argument, including UUID"""
    try:
        pid, source = SourceRecord.get_source_by_pid(uuid)
        if not source or not pid:
            raise Exception('Source not found')
        try:
            with source.current_user_has_publish_permission.require():
                return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                           'ok', 'source', \
                                           {
                                               'record': source_v1.transform_record(pid, source),
                                               'allows': 'publish'
                                           }
                                           )
        except PermissionDenied as err:
            with source.current_user_has_edit_permission.require():
                # # print('*********************************')
                # # print(source)
                # record = source_v1.preprocess_record(pid, source)
                # # print(record)
                # # print('*********************************')
                # record['allows'] = 'edit'
                return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                        'ok', 'source', \
                                        {
                                            'record': source_v1.transform_record(pid,source),
                                            'allows': 'edit'
                                        }
                                       )

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
            # print(dd)
            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                       'ok', 'versions', \
                                       dd)
    except Exception as e:
        # print()
        return iroko_json_response(IrokoResponseStatus.ERROR, traceback.format_exc(), None, None)




@api_blueprint.route('/<uuid>/unpublish', methods=['POST'])
@require_api_auth()
def source_unpublish(uuid):
    # pone source_status = SourceStatus.TO_REVIEW
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')

        with source.current_user_has_publish_permission.require():
            source['source_status'] = SourceStatus.TO_REVIEW.value
            source.update()

            # TODO: aqui hay un error con los get managers
            # notification = NotificationSchema()
            # notification.classification = NotificationType.INFO
            # notification.description = _('Se ha despublicado la fuente: {0}.'.format(source['name']))
            # notification.emiter = _('Sistema')
            #
            # for user in source.get_managers:
            #     notification.receiver_id = user
            #     Notifications.new_notification(notification)
            # print('************************** to response')
            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'source',
                                       source)
    except PermissionDenied as err:
        msg = 'Permission denied for changing source'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        raise e
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/me/<status>')
@require_api_auth()
def get_current_user_sources(status):
    """
        returns the sources of wich current_user is manager
        param status: 'ALL', 'APPROVED', 'TO_REVIEW', 'UNOFFICIAL'
    """

    # print("## start get sources {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))
    try:
        # count = int(request.args.get('size')) if request.args.get('size') else 10
        # page = int(request.args.get('page')) if request.args.get('page') else 1
        #
        # if page < 1:
        #     page = 1
        # offset = count * (page - 1)
        # limit = offset + count
        # # print(offset)
        # # print(limit)
        # print(status)
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
            # # print(search_result)
            # # print(source_data_schema_many.dump(search_result))

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

        # # print("## iroko_json_response {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))
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
        # print('source> ', source)
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


@api_blueprint.route('/stats', methods=['GET'])
def get_sources_stats():
    """

    """

    # TODO:
    # 1- obtener de cuor, la organizacion con los hijos.
    # result = dict()
    # result['id'] = 'orgID'
    # 2- por cada uno de los hijos de la organizacion
    #  por ahora esta bien asi
    try:
        # # print("************************** START get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))

        search = SourceSearch()
        org = dict()

        offset = request.args.get('offset') if request.args.get('offset') else 3

        # top organization bucket
        org_id = request.args.get('org') if request.args.get('org') else None
        if org_id:
            org = CuorHelper.query_cuor_by_uuid(org_id)
            # # print('******************* ORG *******************',org)
            if not org or 'metadata' not in org:
                org_id = None
                org = {}
                # raise Exception('Organization with ID: {0} not found'.format(org_id))
        if org_id:
            search = search.filter('term', organizations__id=org_id)
            bucket_org = A('terms', field='organizations.id', size=999999)
            search.aggs.bucket('orgs', bucket_org)

        # # print("************************** CUOR REQUEST get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))


        # classification bucket
        # subjects
        # vocab = Vocabulary.query.filter_by(identifier=IrokoVocabularyIdentifiers.SUBJECTS.value).first()
        subjects_terms = Term.query.filter_by(vocabulary_id=IrokoVocabularyIdentifiers.SUBJECTS.value, parent_id=None).all()
        subjects = term_schema_many.dump(subjects_terms) #erm_node_schema.dump_term_node_list(subjects_terms, 0, 0)
        # indexes
        # vocab = Vocabulary.query.filter_by(identifier=IrokoVocabularyIdentifiers.INDEXES.value).first()
        indexes_terms = Term.query.filter_by(vocabulary_id=IrokoVocabularyIdentifiers.INDEXES.value, parent_id=None).all()
        indexes = term_schema_many.dump(indexes_terms) #term_node_schema.dump_term_node_list(indexes_terms, 0, 0)

        # bucket
        bucket_classifications = A('terms', field='classifications.id', size=999999)
        search.aggs.bucket('classifications', bucket_classifications)

        # source_type bucket
        source_types = []
        for k in SourceType:
            source_types.append({
                'source_type': k.value
            })
            # print(k.value, '*****')
        bucket_source_type = A('terms', field='source_type', size=999999)
        search.aggs.bucket('source_type', bucket_source_type)

        # # print(
        #     "************************** SEARCH EXEC get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))
        search.sort('_save_info_updated')
        response = search[0:offset].execute()

        hits = []
        for hit in response.hits:
            hits.append(
                {
                    'id':                hit['id'],
                    'name':              hit['name']
                }
            )

        # # print("************************** MI COSA get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))

        if org_id:
            org['metadata']['source_count'] = search.count()
            for item in response.aggregations.orgs.buckets:
                # print('****** org ******', item.doc_count, item.key)
                CuorHelper.append_key_value_to_relationship(org, item.key, 'child', 'source_count', item.doc_count)

        for item in response.aggregations.classifications.buckets:
            # print('****** class ******', item.doc_count, item.key)
            for term in subjects:
                # print('************ term ', term['uuid'])
                if str(term['uuid']) == item.key:
                    term['source_count'] = item.doc_count
            for term in indexes:
                # print('************ term ', term['uuid'])
                if str(term['uuid']) == item.key:
                    term['source_count'] = item.doc_count

        for item in response.aggregations.source_type.buckets:
            for t in source_types:
                if t['source_type'] == item.key:
                    t['source_count'] = item.doc_count

        # # print("************************** END get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                   'ok', 'aggr', \
                                   {
                                       'sources_count': search.count(),
                                       'last_sources': hits,
                                       'org': org,
                                       'subjects': subjects,
                                       'indexes': indexes,
                                       'source_types': source_types
                                   })
    except Exception as e:
        raise e
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
