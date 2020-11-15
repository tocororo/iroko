#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
"""Iroko sources api views."""


from __future__ import absolute_import, print_function

import datetime
import traceback

from elasticsearch_dsl import A
from flask import Blueprint, request
from flask_login import current_user
from flask_principal import PermissionDenied
from invenio_access import ActionUsers
from invenio_accounts.models import User
from invenio_cache import current_cache
from invenio_db import db
from invenio_oauth2server import require_api_auth
from invenio_pidstore.errors import PIDObjectAlreadyAssigned

from iroko.sources.api import (
    SourceRecord, IrokoSourceVersions,
)
from iroko.sources.marshmallow.source import (
    source_version_schema, source_version_schema_many,
)
from iroko.sources.marshmallow.source_v1 import source_v1_response, source_v1
from iroko.sources.models import SourceStatus, SourceType
from iroko.sources.permissions import (
    is_user_sources_admin, ObjectSourceOrganizationManager, ObjectSourceTermManager,
    get_arguments_for_source_from_action,
    ObjectSourceManager,
    ObjectSourceEditor,
    user_is_term_manager,
    user_is_organization_manager,
    get_user_ids_for_source_from_action,
)
from iroko.sources.search import SourceSearch
from iroko.userprofiles import UserProfile
from iroko.userprofiles.marshmallow import user_schema_many
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
            with db.session.begin_nested():
                db.session.add(ActionUsers.allow(ObjectSourceEditor(source.id), user=current_user))
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

        if source.user_has_edit_permission(current_user):
            # si no esta aprobada significa que siempre es la current.
            # si esta aprobada el proceso es otro
            # print(input_data)

            data = dict(input_data['data'])
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

        if source.user_has_manager_permission(current_user):

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


@api_blueprint.route('/<uuid>/unpublish', methods=['POST'])
@require_api_auth()
def source_unpublish(uuid):
    # pone source_status = SourceStatus.TO_REVIEW
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')

        if source.user_has_manager_permission(current_user):
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
        print(dict(source))
        try:
            if source.user_has_manager_permission(current_user):
                return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                           'ok', 'source', \
                                           {
                                               'record': source_v1.transform_record(pid, source),
                                               'allows': 'publish'
                                           }
                                           )
        except PermissionDenied as err:
            if source.user_has_edit_permission(current_user):
                # # print('*********************************')
                # # print(source)
                # record = source_v1.preprocess_record(pid, source)
                # # print(record)
                # # print('*********************************')
                # record['allows'] = 'edit'
                return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                           'ok', 'source', \
                                           {
                                               'record': source_v1.transform_record(pid, source),
                                               'allows': 'edit'
                                           }
                                           )

    except Exception as e:
        print(traceback.format_exc())
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/<uuid>/versions', methods=['GET'])
@require_api_auth()
def get_source_versions(uuid):
    """Get all source versions by source UUID, with permission checking"""

    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Source not found')

        if source.user_has_edit_permission(current_user):
            versions = IrokoSourceVersions.get_versions(uuid)
            dd = source_version_schema_many.dump(versions)
            # print(dd)
            return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                                       'ok', 'versions', \
                                       dd)
    except Exception as e:
        # print()
        return iroko_json_response(IrokoResponseStatus.ERROR, traceback.format_exc(), None, None)


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
            # TODO: hay que buscar una manera de hacerlo por aqui:
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
        sources_terms = get_arguments_for_source_from_action(current_user, 'source_term_manager_actions')
        terms = Term.query.filter(Term.uuid.in_(sources_terms)).all()

        sources_orgs = get_arguments_for_source_from_action(current_user, 'source_organization_manager_actions')
        orgs = []
        for org in sources_orgs:
            orgs.append(CuorHelper.query_cuor_by_uuid(org))

        response = iroko_json_response(
            IrokoResponseStatus.SUCCESS,
            'ok',
            'sources',
            {
                'manager':       manager,
                'editor':        editor,
                'terms':         term_schema_many.dump(terms),
                'organizations': orgs,
                'admin':         is_user_sources_admin(current_user)
            }
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

        if source.user_has_edit_permission(current_user):
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


def _get_sources_stats(org_id, offset):
    # TODO:
    # 1- obtener de cuor, la organizacion con los hijos.
    # result = dict()
    # result['id'] = 'orgID'
    # 2- por cada uno de los hijos de la organizacion
    #  por ahora esta bien asi

    # print("************************** START get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))

    search = SourceSearch()
    org = dict()

    if org_id:
        org = CuorHelper.query_cuor_by_uuid(org_id)
        # print('******************* ORG *******************',org)
        if not org or 'metadata' not in org:
            org_id = None
            org = {}
            # raise Exception('Organization with ID: {0} not found'.format(org_id))
    if org_id:
        search = search.filter('term', organizations__id=org_id)
        bucket_org = A('terms', field='organizations.id', size=999999)
        search.aggs.bucket('orgs', bucket_org)

    # print("************************** CUOR REQUEST get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))

    # classification bucket
    # subjects
    # vocab = Vocabulary.query.filter_by(identifier=IrokoVocabularyIdentifiers.SUBJECTS.value).first()
    subjects_terms = Term.query.filter_by(vocabulary_id=IrokoVocabularyIdentifiers.SUBJECTS.value,
                                          parent_id=None).all()
    subjects = term_schema_many.dump(subjects_terms)  # erm_node_schema.dump_term_node_list(subjects_terms, 0, 0)
    # indexes
    # vocab = Vocabulary.query.filter_by(identifier=IrokoVocabularyIdentifiers.INDEXES.value).first()
    indexes_terms = Term.query.filter_by(vocabulary_id=IrokoVocabularyIdentifiers.INDEXES.value,
                                         parent_id=None).all()
    indexes = term_schema_many.dump(indexes_terms)  # term_node_schema.dump_term_node_list(indexes_terms, 0, 0)

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

    # print("************************** SEARCH EXEC get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))
    search.sort('_save_info_updated')
    response = search[0:offset].execute()

    hits = []
    for hit in response.hits:
        hits.append(
            {
                'id':   hit['id'],
                'name': hit['name']
            }
        )

    # print("************************** MI COSA get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))

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

    # print("************************** END get aggr {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))

    result = {
        'sources_count': search.count(),
        'last_sources':  hits,
        'org':           org,
        'subjects':      subjects,
        'indexes':       indexes,
        'source_types':  source_types
    }
    return result


@api_blueprint.route('/stats', methods=['GET'])
def get_sources_stats():
    """

    """
    try:

        offset = request.args.get('offset') if request.args.get('offset') else 3

        # top organization bucket
        org_id = request.args.get('org') if request.args.get('org') else None

        cache = current_cache.get("get_sources_stats:{0}{1}".format(org_id, offset)) or {}
        if "date" not in cache:
            cache["date"] = datetime.datetime.now()
        if datetime.datetime.now() - cache["date"] < datetime.timedelta(days=1) and "stats" in cache:
            print("USING CACHE STATS")
            result = cache["stats"]
            return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok', 'aggr', result)
        else:
            result = _get_sources_stats(org_id, offset)
            cache["date"] = datetime.datetime.now()
            cache["stats"] = result
            current_cache.set("get_sources_stats:{0}{1}".format(org_id, offset), cache, timeout=-1)
            return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok', 'aggr', result)

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/permission/editor/<uuid>/users', methods=['GET'])
@require_api_auth()
def get_users_source_editor(uuid):
    """
    get the lists of user with permission of editor and manager
    :param uuid: source uuid
    :return:
    """
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')

        if source.user_has_manager_permission(current_user):
            ids = get_user_ids_for_source_from_action('source_editor_actions', uuid)
            users = User.query.filter(User.id.in_(ids)).all()
            return iroko_json_response(
                IrokoResponseStatus.SUCCESS,
                'ok',
                'permission',
                {
                    'action': 'editor',
                    'source': uuid,
                    'users':  user_schema_many.dump(users)
                }

            )

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/permission/manager/<uuid>/users', methods=['GET'])
@require_api_auth()
def get_users_source_manager(uuid):
    """
    get the lists of user with permission of editor and manager
    :param uuid: source uuid
    :return:
    """
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')

        if source.user_has_manager_permission(current_user):
            ids = get_user_ids_for_source_from_action('source_manager_actions', uuid)
            users = User.query.filter(User.id.in_(ids)).all()
            return iroko_json_response(
                IrokoResponseStatus.SUCCESS,
                'ok',
                'permission',
                {
                    'action': 'manager',
                    'source': uuid,
                    'users':  user_schema_many.dump(users)
                }

            )
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/permission/organization/<uuid>/users', methods=['GET'])
@require_api_auth()
def get_users_organization(uuid):
    """
    get the list of user with permission of organization manager
    :param uuid: organization uuid
    :return:
    """
    try:
        org = CuorHelper.query_cuor_by_uuid(uuid)
        if not org:
            raise Exception('Organization not found')

        if is_user_sources_admin(current_user) or \
            user_is_organization_manager(org['id'], current_user):
            ids = get_user_ids_for_source_from_action('source_organization_manager_actions', uuid)
            users = User.query.filter(User.id.in_(ids)).all()
            return iroko_json_response(
                IrokoResponseStatus.SUCCESS,
                'ok',
                'permission',
                {
                    'action':       'manager',
                    'organization': uuid,
                    'users':        user_schema_many.dump(users)
                }

            )
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/permission/term/<uuid>/users', methods=['GET'])
@require_api_auth()
def get_users_term(uuid):
    """
    get the lists of user with permission of term manager
    :param uuid: term uuid
    :return:
    """
    try:
        term = Term.query.filter_by(uuid=uuid).first()
        if not term:
            raise Exception('Term not found')

        if is_user_sources_admin(current_user) or \
            user_is_term_manager(term.uuid, current_user):
            ids = get_user_ids_for_source_from_action('source_term_manager_actions', uuid)
            users = User.query.filter(User.id.in_(ids)).all()
            return iroko_json_response(
                IrokoResponseStatus.SUCCESS,
                'ok',
                'permission',
                {
                    'action': 'manager',
                    'term':   uuid,
                    'users':  user_schema_many.dump(users)
                }

            )
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/permission/<user>/editor/<uuid>/allow', methods=['POST'])
@require_api_auth()
def set_source_editor_allow(user, uuid):
    return set_source_editor(user, uuid, True)


@api_blueprint.route('/permission/<user>/editor/<uuid>/deny', methods=['POST'])
@require_api_auth()
def set_source_editor_deny(user, uuid):
    return set_source_editor(user, uuid, False)


def set_source_editor(user, uuid, allow=False):
    """
    Set user as editor of a source
    :param uuid: source uuid
    :param user: user id
    :param allow: if allow or deny
    :return:
    """
    try:
        offset = request.args.get('offset') if request.args.get('offset') else 3
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')
        userObj = User.query.filter_by(id=user).first()
        if not userObj:
            raise Exception('User not found')

        if source.user_has_manager_permission(current_user):
            with db.session.begin_nested():
                ActionUsers.query.filter_by(user_id=user, action='source_editor_actions',
                                            argument=uuid).delete()
                if allow:
                    db.session.add(ActionUsers.allow(ObjectSourceEditor(uuid), user=userObj))
                else:
                    db.session.add(ActionUsers.deny(ObjectSourceEditor(uuid), user=userObj))
            db.session.commit()
            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'permission',
                                       {
                                           'source':     uuid,
                                           'user':       user,
                                           'permission': 'editor',
                                           'allow':      allow
                                       })
        raise PermissionDenied()

    except PermissionDenied as err:
        msg = 'Permission denied'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/permission/<user>/manager/<uuid>/allow', methods=['POST'])
@require_api_auth()
def set_source_manager_allow(user, uuid):
    return set_source_manager(user, uuid, True)


@api_blueprint.route('/permission/<user>/manager/<uuid>/deny', methods=['POST'])
@require_api_auth()
def set_source_manager_deny(user, uuid):
    return set_source_manager(user, uuid, False)


def set_source_manager(user, uuid, allow=False):
    """
    Set user as manager of a source
    :param uuid: source uuid
    :param user: user id
    :param allow: if allow or deny
    :return:
    """
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')
        userObj = User.query.filter_by(id=user).first()
        if not userObj:
            raise Exception('User not found')
        if source.user_has_manager_permission(current_user):
            with db.session.begin_nested():
                ActionUsers.query.filter_by(user_id=user, action='source_manager_actions',
                                            argument=uuid).delete()
                if allow:
                    db.session.add(ActionUsers.allow(ObjectSourceManager(uuid), user=userObj))
                else:
                    db.session.add(ActionUsers.deny(ObjectSourceManager(uuid), user=userObj))
            db.session.commit()
            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'permission',
                                       {
                                           'term':       uuid,
                                           'user':       user,
                                           'permission': 'manager',
                                           'allow':      allow
                                       })

        raise PermissionDenied()

    except PermissionDenied as err:
        msg = 'Permission denied'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/permission/<user>/organization/<uuid>/allow', methods=['POST'])
@require_api_auth()
def set_organization_manager_allow(user, uuid):
    return set_organization_manager(user, uuid, True)


@api_blueprint.route('/permission/<user>/organization/<uuid>/deny', methods=['POST'])
@require_api_auth()
def set_organization_manager_deny(user, uuid):
    return set_organization_manager(user, uuid, False)


def set_organization_manager(user, uuid, allow=False):
    """
    Set user as manager of a organization
    :param uuid: organization or term uuid
    :param user: user id
    :param allow: if allow or deny
    :return:
    """
    try:
        userObj = User.query.filter_by(id=user).first()
        if not userObj:
            raise Exception('User not found')
        org = CuorHelper.query_cuor_by_uuid(uuid)
        if not org:
            raise Exception('Organization not found')
        parents = CuorHelper.get_relationships_parent(org)
        print(parents)
        allow_parent = False
        for p in parents:
            try:
                allow_parent = user_is_organization_manager(p['id'], current_user)
            except PermissionDenied:
                pass

        if is_user_sources_admin(current_user) or \
            allow_parent or \
            user_is_organization_manager(org['id'], current_user):
            with db.session.begin_nested():
                ActionUsers.query.filter_by(user_id=user, action='source_organization_manager_actions',
                                            argument=uuid).delete()
                if allow:
                    db.session.add(ActionUsers.allow(ObjectSourceOrganizationManager(uuid), user=userObj))
                else:
                    db.session.add(ActionUsers.deny(ObjectSourceOrganizationManager(uuid), user=userObj))
            db.session.commit()
            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'permission',
                                       {
                                           'org':        uuid,
                                           'user':       user,
                                           'permission': 'manager',
                                           'allow':      allow
                                       })

        raise PermissionDenied()

    except PermissionDenied as err:
        msg = 'Permission denied'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/permission/<user>/term/<uuid>/allow', methods=['POST'])
@require_api_auth()
def set_term_manager_allow(user, uuid):
    return set_term_manager(user, uuid, True)


@api_blueprint.route('/permission/<user>/term/<uuid>/deny', methods=['POST'])
@require_api_auth()
def set_term_manager_deny(user, uuid):
    return set_term_manager(user, uuid, False)


def set_term_manager(user, uuid, allow=False):
    """
    Set user as manager of a organization
    :param uuid: organization or term uuid
    :param user: user id
    :param allow: if allow or deny
    :return:
    """
    try:
        userObj = User.query.filter_by(id=user).first()
        if not userObj:
            raise Exception('User not found')
        term = Term.query.filter_by(uuid=uuid).first()
        if not term:
            raise Exception('Term not found')
        parent = None
        if term.parent_id:
            parent = Term.query.filter_by(id=term.parent_id).first()

        if is_user_sources_admin(current_user) or \
            user_is_term_manager(term.uuid, current_user) or \
            (parent and user_is_term_manager(parent.uuid, current_user)):

            with db.session.begin_nested():
                ActionUsers.query.filter_by(user_id=user, action='source_term_manager_actions',
                                            argument=uuid).delete()
                if allow:
                    db.session.add(ActionUsers.allow(ObjectSourceTermManager(uuid), user=userObj))
                else:
                    db.session.add(ActionUsers.deny(ObjectSourceTermManager(uuid), user=userObj))
            db.session.commit()
            return iroko_json_response(IrokoResponseStatus.SUCCESS,
                                       'ok', 'permission',
                                       {
                                           'term':       uuid,
                                           'user':       user,
                                           'permission': 'manager',
                                           'allow':      allow
                                       })

        raise PermissionDenied()

    except PermissionDenied as err:
        msg = 'Permission denied'
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)
    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
