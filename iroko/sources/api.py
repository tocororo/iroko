#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import traceback
from datetime import date, datetime
from typing import Dict
from uuid import uuid4

from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl.query import Bool, Q
from flask_login import current_user
from invenio_access.models import ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_jsonschemas import current_jsonschemas
from invenio_pidstore.errors import PIDDeletedError, PIDDoesNotExistError
from invenio_pidstore.models import PIDStatus, PersistentIdentifier
from invenio_pidstore.resolver import Resolver

from invenio_records_files.api import Record

from invenio_records_rest.views import lt_es7
from invenio_rest.serializer import result_wrapper
from sqlalchemy import desc, func
from sqlalchemy.orm.exc import NoResultFound

import iroko.pidstore.minters as iroko_minters
import iroko.pidstore.pids as pids
import iroko.pidstore.providers as iroko_providers
from iroko.api import IrokoBaseRecord
from iroko.harvester.models import HarvestType, Repository
from iroko.pidstore.pids import identifiers_schemas
from iroko.sources.journals.utils import field_is_in_data, issn_is_in_data
from iroko.sources.models import Source, SourceStatus, SourceVersion, TermSources
from iroko.sources.permissions import (
    get_arguments_for_source_from_action, get_user_ids_for_source_from_action,
    is_user_sources_admin, user_has_edit_permission, user_has_manager_permission,
    )
from iroko.sources.search import SourceSearch
from iroko.sources.utils import _load_terms_tree
from iroko.utils import IrokoVocabularyIdentifiers
from iroko.vocabularies.api import Terms
from iroko.vocabularies.models import Term


class SourceRecord(IrokoBaseRecord):
    # TODO: en algunos casos hace falta hacer PATCH en vez de UPDATE.
    # por ejemplo, cuando vienen los datos de issn.org

    _schema = "sources/source-v1.0.0.json"

    def __str__(self):
        return self['title']

    @classmethod
    def new_source_revision(cls, data, user_id=None, comment='no comment'):

        if data and \
            (data['source_status'] == SourceStatus.UNOFFICIAL.value or
             data['source_status'] == SourceStatus.TO_REVIEW.value):

            data['_save_info'] = {
                'user_id': str(user_id),
                'comment': str(comment),
                'updated': str(date.today()),
                }
            new_source, msg = SourceRecord.create_or_update(data, None, True, True)
            print('now we are here....')
            # msg, new_source = Sources.insert_new_source(source, SourceStatus.UNOFFICIAL,
            # user=user)

            # if 'oaiurl' in data:
            #     repo = Repository.query.filter_by(source_uuid=new_source.id).first()
            #     if not repo:
            #         repo = Repository()
            #         repo.source_uuid = new_source.id
            #     repo.harvest_endpoint = data['oaiurl']
            #     repo.harvest_type = HarvestType.OAI
            #     db.session.add(repo)

            IrokoSourceVersions.new_version(
                new_source.id, data, user_id=user_id, comment=comment,
                is_current=True
                )
            return 'ok', new_source
        else:
            return 'Bad input data:{0}'.format(data), None

    @classmethod
    def create_or_update(cls, data, source_uuid=None, dbcommit=False, reindex=False, **kwargs):
        """Create or update IrokoRecord.
        This method bypass all SourceVersion and approval process of a Source.
        Use with care
        """
        resolver = Resolver(
            pid_type=pids.SOURCE_UUID_PID_TYPE,
            object_type=pids.IROKO_OBJECT_TYPE,
            getter=cls.get_record,
            )
        if source_uuid:
            # if uuid is in
            try:
                persistent_identifier, source = resolver.resolve(str(source_uuid))
                if source:
                    # print("{0}={1} found".format(pids.SOURCE_UUID_PID_TYPE, source_uuid))
                    source.update(data, dbcommit=dbcommit, reindex=reindex)
                    return source, 'updated'
            except (PIDDeletedError, NoResultFound) as ex:
                cls.delete_pid_without_object(pids.SOURCE_UUID_PID_TYPE, str(source_uuid))
                # print('#### cls.delete_all_pids_without_object(data[pids.IDENTIFIERS_FIELD])')
            except PIDDoesNotExistError as pidno:
                # print("PIDDoesNotExistError:  {0} == {1}".format(pids.SOURCE_UUID_PID_TYPE,
                # str(source_uuid)))
                pass
            except Exception as e:
                # print('-------------------------------')
                # # print(str(e))
                # print(traceback.format_exc())
                # print('-------------------------------')
                pass
                # source = cls.get_source_by_pid(source_uuid, with_deleted=False)
            # print('!!!!!!!!!!!!!!!!!!!!!!! ', data)
        if pids.IDENTIFIERS_FIELD in data:
            # if not uuid, find any persistent identifier in data.
            print("find identifiers in data", data[pids.IDENTIFIERS_FIELD])
            for identifier in data[pids.IDENTIFIERS_FIELD]:
                try:
                    pid_type = identifier[pids.IDENTIFIERS_FIELD_TYPE]
                    pid_value = identifier[pids.IDENTIFIERS_FIELD_VALUE]
                    resolver.pid_type = pid_type
                    print("{0}={1} find".format(pid_type, pid_value))
                    persistent_identifier, source = resolver.resolve(pid_value)
                    if source:
                        print("{0}={1} found".format(pid_type, pid_value))
                        return source.update(data, dbcommit=dbcommit, reindex=reindex), 'updated'
                        print('update was done!!!')
                        #  'updated'
                except PIDDoesNotExistError as pidno:
                    print("PIDDoesNotExistError:  {0} == {1}".format(pid_type, pid_value))
                    pass
                except (PIDDeletedError, NoResultFound) as ex:
                    cls.delete_pid_without_object(pid_type, pid_value)
                except Exception as e:
                    # print('-------------------------------')
                    # print(str(e))
                    print(traceback.format_exc())
                    # print('-------------------------------')
                    pass

        # if here, means any persisten identifier is not created, so, create the source!!!
        # print("no pids found, create source")
        source_uuid = uuid4()
        data[pids.IROKO_UUID_FIELD] = str(source_uuid)
        created_source = cls.create(data, id_=source_uuid, dbcommit=dbcommit, reindex=reindex)
        return created_source, 'created'

    @classmethod
    def delete_pid_without_object(cls, pid_type, pid_value):

        try:
            pid_item = PersistentIdentifier.get(pid_type, pid_value)
            pid_item.status = PIDStatus.NEW
            # # print('getting pid item: ')
            if pid_item.delete():
                db.session.commit()
            # print("***************** DELETED!!!!")
        except PIDDoesNotExistError:
            # print('PIDDoesNotExistError: {0} - {1}'.format(pid_type, pid_value))
            pass
        except Exception as e:
            # print("-------- DELETING PID ERROR ------------")
            # print(traceback.format_exc())
            pass

    @classmethod
    def delete_all_pids_without_object(cls, pid_list):
        try:
            # print('pids list: ')
            # print(pid_list)
            if pid_list and len(pid_list) > 0:
                for identifier in pid_list:
                    try:
                        pid_type = identifier[pids.IDENTIFIERS_FIELD_TYPE]
                        pid_value = identifier[pids.IDENTIFIERS_FIELD_VALUE]
                        # # print('pid type deleting: ')
                        # # print(pid_type)
                        # # print(pid_value)
                        pid_item = PersistentIdentifier.get(pid_type, pid_value)
                        pid_item.status = PIDStatus.NEW
                        # # print('getting pid item: ')
                        if pid_item.delete():
                            db.session.commit()
                        # # print("***************** DELETED!!!!")
                    except PIDDoesNotExistError:
                        # print('PIDDoesNotExistError: {0} - {1}'.format(pid_type, pid_value))
                        pass
        except Exception as e:
            # print("-------- DELETING PID ERROR ------------")
            # print(traceback.format_exc())
            pass

    @classmethod
    def create(cls, data, id_, dbcommit=False, reindex=False, **kwargs):
        """Create a new SourceRecord."""
        data['$schema'] = current_jsonschemas.path_to_url(cls._schema)
        assert pids.IROKO_UUID_FIELD in data
        assert id_

        data['_save_info_updated'] = str(date.today())

        # print('%%%%%%%%%')
        iroko_minters.iroko_source_uuid_minter(id_, data)
        # print('%%%%%%%%%')
        iroko_minters.iroko_record_identifiers_minter(id_, data, pids.IROKO_OBJECT_TYPE)
        # print('%%%%%%%%%')
        # jj = json.dumps(data, ensure_ascii=False)
        source = super(SourceRecord, cls).create(data=data, id_=id_, **kwargs)
        # print('%%%%%%%%%')
        if dbcommit:
            source.dbcommit(reindex)
        return source

    @classmethod
    def delete(cls, data, delindex=True, force=False):
        """Delete a IrokoRecord record."""
        assert data.get(pids.IROKO_UUID_FIELD)
        pid = data.get(pids.IROKO_UUID_FIELD)
        source = cls.get_source_by_pid(pid, with_deleted=False)
        # pid.delete()
        if source:
            result = super(SourceRecord, source).delete(force=force)
            # result = source.delete(force=force)
            if delindex:
                try:
                    RecordIndexer().delete(source)
                except NotFoundError:
                    pass

            return result
        return False

    @classmethod
    def get_source_by_pid_in_data(cls, data):
        """
        Try to find a source by any identifier in data.
        :param data: data must have 'identifiers' field.
        :return:
        """
        resolver = Resolver(
            pid_type=pids.SOURCE_UUID_PID_TYPE,
            object_type=pids.IROKO_OBJECT_TYPE,
            getter=cls.get_record,
            )
        if pids.IDENTIFIERS_FIELD in data:
            # if not uuid, find any persistent identifier in data.
            # print("find identifiers in data", data[pids.IDENTIFIERS_FIELD])
            for identifier in data[pids.IDENTIFIERS_FIELD]:
                try:
                    pid_type = identifier[pids.IDENTIFIERS_FIELD_TYPE]
                    pid_value = identifier[pids.IDENTIFIERS_FIELD_VALUE]
                    resolver.pid_type = pid_type
                    persistent_identifier, source = resolver.resolve(pid_value)
                    pid = PersistentIdentifier.get(pids.SOURCE_UUID_PID_TYPE, source['id'])
                    return pid, source
                except Exception:
                    pass
        return None, None

    @classmethod
    def get_source_by_pid(cls, pid_value, with_deleted=False):
        resolver = Resolver(
            pid_type=pids.SOURCE_UUID_PID_TYPE,
            object_type=pids.IROKO_OBJECT_TYPE,
            getter=cls.get_record,
            )
        try:
            return resolver.resolve(str(pid_value))
        except Exception:
            pass

        for pid_type in identifiers_schemas:
            try:
                resolver.pid_type = pid_type
                schemapid, source = resolver.resolve(pid_value)
                pid = PersistentIdentifier.get(pids.SOURCE_UUID_PID_TYPE, source['id'])
                return pid, source

            except Exception as e:
                pass
        return None, None

    def new_revision(self, user_id=None, comment='no comment'):
        self['_save_info'] = {
            'user_id': str(user_id),
            'comment': str(comment),
            'updated': str(date.today()),
            }
        self.update()
        IrokoSourceVersions.new_version(
            self.id, dict(self), user_id=user_id, comment=comment,
            is_current=True
            )

    def update(self, data=None, dbcommit=True, reindex=True):
        """Update data for record."""
        print('begin update')
        old = dict(self)

        if data and type(data) == dict:
            # print('super(SourceRecord, self).update(data)')
            super(SourceRecord, self).update(data)

            # if 'organizations' in old:
            #     for org in old['organizations']:
            #         self.add_update_item_to_list_field('organizations', 'id', org)
            # if 'organizations' in data:
            #     for org in data['organizations']:
            #         self.add_update_item_to_list_field('organizations', 'id', org)
            #
            # if 'classifications' in old:
            #     for term in old['classifications']:
            #         self.add_update_item_to_list_field('classifications', 'id', term)
            # if 'classifications' in data:
            #     for term in data['classifications']:
            #         self.add_update_item_to_list_field('classifications', 'id', term)
            #
            # if pids.IDENTIFIERS_FIELD in old:
            #     for _id in old[pids.IDENTIFIERS_FIELD]:
            #         self.add_update_item_to_list_field(pids.IDENTIFIERS_FIELD, 'idtype', _id)
            # if pids.IDENTIFIERS_FIELD in data:
            #     for _id in data[pids.IDENTIFIERS_FIELD]:
            #         self.add_update_item_to_list_field(pids.IDENTIFIERS_FIELD, 'idtype', _id)

        print('update pids ')
        self._update_pids()

        self['_save_info_updated'] = str(date.today())

        self._update_repo_info()

        super(SourceRecord, self).commit()

        if dbcommit:
            self.dbcommit(reindex)

        print('UPDATED', self.model.json)
        return self

    def _update_repo_info(self):
        if pids.IDENTIFIERS_FIELD in self.model.json:
            for identifier in self.model.json[pids.IDENTIFIERS_FIELD]:
                pid_type = identifier[pids.IDENTIFIERS_FIELD_TYPE]
                pid_value = identifier[pids.IDENTIFIERS_FIELD_VALUE]
                if pid_type == 'oaiurl' and pid_value:
                    repo = Repository.query.filter_by(source_uuid=self.id).first()
                    if not repo:
                        repo = Repository()
                        repo.source_uuid = self.id
                        db.session.add(repo)
                    repo.harvest_endpoint = pid_value
                    repo.harvest_type = HarvestType.OAI
                    db.session.commit()
                    # self['repo'] = {
                    #     'harvest_type':  repo.harvest_type.value,
                    #     'harvest_endpoint': repo.harvest_endpoint,
                    #     'last_harvest_run': repo.last_harvest_run,
                    #     'status':  re.status.value
                    # }

    def _update_pids(self):
        newPids = []
        # TODO: que pasa si se eliminan PIDS? !!!!!
        if pids.IDENTIFIERS_FIELD in self:
            for ids in self[pids.IDENTIFIERS_FIELD]:
                if ids['idtype'] in identifiers_schemas:
                    if ids['value'] != '':
                        try:
                            pid = PersistentIdentifier.get(ids['idtype'], ids['value'])
                            obj_uuid = pid.get_assigned_object(pids.IROKO_OBJECT_TYPE)
                            print('!!!!!!!')
                            print('{0}-{1}'.format(ids['idtype'], ids['value']))
                            print('!!!!!!!')
                            if obj_uuid != self.id:
                                print('!!!!!!!******')
                                print(
                                    'PIDObjectAlreadyAssigned{0}-{1}'.format(
                                        ids['idtype'], ids['value']
                                        )
                                    )
                                # TODO: pensar esto, lo borro, pero no aviso...
                                self[pids.IDENTIFIERS_FIELD].remove(ids)
                        # except PIDObjectAlreadyAssigned as e:
                        #     print('!!!!!!! what?')
                        #     raise e
                        except PIDDoesNotExistError:
                            iroko_providers.IrokoRecordsIdentifiersProvider.create_pid(
                                ids['idtype'], ids['value'],
                                object_type=pids.IROKO_OBJECT_TYPE,
                                object_uuid=self.id, data=self
                                )
                    else:
                        self[pids.IDENTIFIERS_FIELD].remove(ids)
                else:
                    self[pids.IDENTIFIERS_FIELD].remove(ids)

    # def _add_update_item_to_list(self, list_key, list_item_id_key, item_to_add):
    #     """add or update an item to a list field of the record.
    #     list_key: the name of the field list in the record
    #     list_item_id_key: the name of the identifier field in the list field
    #     item_to_add: item to add or update to the list.
    #     """
    #     if list_key not in self:
    #         self[list_key] = []
    #     if type(self[list_key]) == list:
    #         for item in self[list_key]:
    #             if type(item) == dict() and item[list_item_id_key] == item_to_add[list_item_id_key]:
    #                 item.update(item_to_add)
    #                 return
    #             elif item == item_to_add:
    #                 return
    #         self[list_key].append(item_to_add)


    @property
    def status(self):
        self.update()
        return self['source_status']

    def add_organization(self, _id, name, role):
        self.add_update_item_to_list_field(
            'organizations', 'id',
            {
                'id': _id,
                'name': name,
                'role': role
                }
            )

    def add_classification(self, _id, description, vocabulary, data):
        self.add_update_item_to_list_field(
            'classifications', 'id',
            {
                'id': _id,
                'description': description,
                'vocabulary': vocabulary,
                'data': data
                }
            )

    def add_identifier(self, idtype, value):
        self.add_update_item_to_list_field(
            pids.IDENTIFIERS_FIELD, 'idtype',
            {
                'idtype': idtype,
                'value': value
                }
            )

    # Permission methods
    #

    def user_has_edit_permission(self, user: User):
        return user_has_edit_permission(self, user)

    def user_has_manager_permission(self, user: User):
        return user_has_manager_permission(self, user)

    @property
    def get_managers(self):

        all_users = []
        managers = get_user_ids_for_source_from_action('source_manager_actions', self.id)

        if managers:
            all_users.extend(managers)

        for term_source in self.model.json['classifications']:

            term_managers = get_user_ids_for_source_from_action(
                'source_term_manager_actions', term_source['id']
                )

            if term_managers:
                all_users.extend(term_managers)

        for org_source in self.model.json['organizations']:

            org_managers = get_user_ids_for_source_from_action(
                'source_organization_manager_actions', org_source['id']
                )

            if org_managers:
                all_users.extend(org_managers)

        # para obtener al full_manager por si no hay alguien mas
        admins = get_user_ids_for_source_from_action('source_full_manager_actions')
        if admins:
            all_users.extend(admins)

        return all_users

    @property
    def get_editors(self):
        return get_user_ids_for_source_from_action('source_editor_actions', self.id)

    @classmethod
    def get_search(cls, status=None, classifications=None, organizations=None) -> SourceSearch:
        """return a  SourceSearch object with the specified status, classifications and
        organizations
        """

        search = SourceSearch()

        if not lt_es7:
            search = search.extra(track_total_hits=True)

        or_filters = []
        and_filters = []

        if classifications is not None:
            for term in classifications:
                or_filters.append(Q('match', **{'classifications.id': term}))
        if organizations is not None:
            for org in organizations:
                or_filters.append(Q('match', **{'organizations.id': org}))
        if status is not None:
            and_filters.append(Q('match', **{'source_status': status}))

        search.query = Bool(filter=Q('bool', should=or_filters, must=and_filters))
        return search

    @classmethod
    def get_sources_search_of_user_as_editor(cls, user: User, status=None):
        """devuelve las fuentes de las cuales el usuario actual es editor """

        ids = get_arguments_for_source_from_action(user, 'source_editor_actions')
        return cls.get_records(ids)

    @classmethod
    def get_sources_search_of_user_as_manager(cls, user: User, status=None) -> SourceSearch:
        """devuelve las fuentes de las cuales el usuario actual es gestor """

        if is_user_sources_admin(user):
            return cls.get_search(status=status)

        # sources_manager = get_arguments_for_source_from_action(user, 'source_manager_actions')
        # if len(sources_manager) == 0:
        #     sources_manager = None
        sources_terms = get_arguments_for_source_from_action(user, 'source_term_manager_actions')
        if len(sources_terms) == 0:
            sources_terms = None
        sources_orgs = get_arguments_for_source_from_action(
            user, 'source_organization_manager_actions'
            )
        if len(sources_orgs) == 0:
            sources_orgs = None

        if sources_orgs is None and sources_terms is None:
            return None

        return cls.get_search(
            status=status, classifications=sources_terms,
            organizations=sources_orgs
            )

    def get_user_ids_source_editor(self) -> list:
        return get_user_ids_for_source_from_action('source_editor_actions', self.id)

    def get_user_ids_source_managers(self) -> list:
        all_users = []
        managers = get_user_ids_for_source_from_action('source_manager_actions', self.id)

        if managers:
            all_users.extend(managers)

        for term_source in self.model.json['classifications']:

            term_managers = get_user_ids_for_source_from_action(
                'source_term_manager_actions', term_source.id
                )

            if term_managers:
                all_users.extend(term_managers)

        for org_source in self.model.json['organizations']:

            org_managers = get_user_ids_for_source_from_action(
                'source_organization_manager_actions', org_source.id
                )

            if org_managers:
                all_users.extend(org_managers)
        admins = get_user_ids_for_source_from_action('source_full_manager_actions')
        if admins:
            all_users.extend(admins)

        return all_users

    def get_editor_versions_not_reviewed(self):
        # lista las versiones de un source que haya creado un editor, en este caso las del current
        # pero solo las versiones que no han sido revisadas por el gestor, en cuyo caso
        # tendria que simplemente editar la fuente, no la versions y asi agregar nuevas versiones
        #
        versions = SourceVersion.query.filter_by(
            source_uuid=self.id, user=current_user, reviewed=False
            ).order_by(
            desc(SourceVersion.created_at)
            ).all()
        # print('versiosn', versions)

        return versions


class IrokoSourceVersions:
    """class for manipulation of SourceVersion"""

    @classmethod
    def get_version(cls, id) -> SourceVersion:
        return SourceVersion.query.filter_by(id=id).first()

    @classmethod
    def get_versions(cls, source_uuid) -> [SourceVersion]:
        return SourceVersion.query.filter(SourceVersion.source_uuid == source_uuid).order_by(
            SourceVersion.created_at.desc()
            ).all()

    @classmethod
    def new_version(cls, source_uuid, data, user_id=None, comment='no comment', is_current=False):

        if not user_id:
            if not current_user:
                raise Exception('Must be authenticated')
            user_id = current_user.id

        # with db.session.begin_nested():
        if is_current:
            for version in SourceVersion.query.filter(
                SourceVersion.source_uuid == source_uuid
                ).all():
                version.is_current = False

        source_version = SourceVersion()
        source_version.comment = comment
        source_version.source_uuid = source_uuid
        source_version.user_id = user_id
        source_version.is_current = is_current
        source_version.created_at = datetime.now()
        db.session.add(source_version)
        db.session.commit()
        source_version.data = data
        db.session.commit()
        return source_version

    @classmethod
    def set_version_as_current(cls, source_uuid, source_version_id):
        version = SourceVersion.query.filter(
            SourceVersion.source_uuid == source_uuid,
            SourceVersion.id == source_version_id
            ).first()
        if version:
            source = SourceRecord.get_record(source_uuid)
            source.update(version.data, True, True)
            with db.session.begin_nested():
                for v in SourceVersion.query.filter(SourceVersion.source_uuid == source_uuid).all():
                    v.is_current = False
                version.is_current = True
                db.session.commit()


def get_current_user_source_permissions() -> Dict[str, Dict[str, list]]:
    """
    Checks from ActionUsers if current_user has source_full_manager_actions,
    if not,
    1- then sources of the terms he has GESTOR permissions over with action
    source_term_manager_actions,
    or with source_manager_actions,
    2- sources he has EDITOR permissions with source_editor_actions
    """

    vocabularies_ids = []
    if is_user_sources_admin(current_user):
        return 'actions', {'source_full_manager_actions': None}

    actions = ActionUsers.query.filter_by(
        user=current_user,
        exclude=False,
        action='source_term_manager_actions'
        ).all()

    terms = []
    for action in actions:
        terms.append(action.argument)

    all_terms = _load_terms_tree(terms)
    # print('----------------tree : ', all_terms)
    sources = TermSources.query.filter(TermSources.term_id.in_(all_terms)).all()

    sources_manager_ids = []
    for source in sources:
        sources_manager_ids.append(source.sources_id)

    actions = ActionUsers.query.filter_by(
        user=current_user,
        exclude=False,
        action='source_manager_actions'
        ).all()

    for action in actions:
        if action.argument not in sources_manager_ids:
            sources_manager_ids.append(action.argument)

    actions = ActionUsers.query.filter_by(
        user=current_user,
        exclude=False,
        action='source_editor_actions'
        ).all()

    sources_editor_ids = []
    for action in actions:
        sources_editor_ids.append(action.argument)

    return 'actions', {
        'source_manager_actions': sources_manager_ids, 'source_editor_actions': sources_editor_ids
        }


def helper_get_classifications_string(source: SourceRecord) -> str:
    try:
        terms = ''
        for term in source.model.json['classifications']:
            if 'id' in term:
                terms = terms + str(term['id']) + ','
        if terms:
            terms = terms[0:-1]
        return terms
    except Exception:
        return ''


def helper_get_organizations_string(source: SourceRecord) -> str:
    try:
        orgs = ''
        for org in source.model.json['organizations']:
            if 'id' in org:
                orgs = orgs + str(org['id']) + ','
        if orgs:
            orgs = orgs[0:-1]
        return orgs
    except Exception:
        return ''


class SourcesDeprecated:
    """API for manipulation of Sources
    Considering SourceVersion: meanining this class use SourceRecord and SourceVersion model.
    """

    @classmethod
    def sync_source_index(cls):
        """
        insertar/actualizar todos los Sources (SqlAlchemy) como SourceRecord (Invenio Record)
        """
        sources = Source.query.all()
        for source in sources:
            data = source.data
            if not data:
                data = dict()
            data[pids.IROKO_UUID_FIELD] = str(source.uuid)
            data['name'] = source.name
            data['source_type'] = source.source_type.value
            data['source_status'] = source.source_status.value
            data['relations'] = cls._get_relations_to_sync(source.id)
            src, status = SourceRecord.create_or_update(
                source.uuid, data, dbcommit=True, reindex=True
                )

    @classmethod
    def _get_relations_to_sync(cls, source_id):
        relations = TermSources.query.filter_by(sources_id=source_id).all()
        result = []
        for rel in relations:
            term = Term.query.filter_by(id=rel.term_id).first()
            if rel.data == None:
                rel.data = dict()
            result.append(dict(uuid=str(term.uuid), data=rel.data, name=str(term.name)))
            if term.parent_id:
                parent = Term.query.filter_by(id=term.parent_id).first()
                result.extend(cls._get_parent_relations_to_sync(parent))
        return result

    @classmethod
    def _get_parent_relations_to_sync(cls, term: Term):
        result = []
        if term.parent_id:
            parent = Term.query.filter_by(id=term.parent_id).first()
            result.append(dict(uuid=str(term.uuid), data=dict()))
            result.extend(cls._get_parent_relations_to_sync(parent))
        else:
            result.append(dict(uuid=str(term.uuid), data=dict()))
        return result

    @classmethod
    def get_sources_id_list(cls):
        # ids = list(map(lambda x: int(x.id), session.query(Source.id).filter(
        # Source.DDDDDD==trigger).all()))
        return list(
            map(
                lambda x: int(x.id),
                db.session.query(Source.id).filter(
                    Source.source_status == SourceStatus.APPROVED
                    ).all()
                )
            )

    @classmethod
    def get_source_by_id(cls, id=None, uuid=None):
        if id is not None:
            return Source.query.filter_by(id=id).first()
        if uuid is not None:
            # uuid = UUIDType(uuid)
            return Source.query.filter_by(uuid=uuid).first()
        return None

    @classmethod
    def get_source_version_by_id(cls, id=None):
        if id is not None:
            return SourceVersion.query.filter_by(id=id).first()
        return None

    @classmethod
    def count_sources(cls):
        return Source.query.count()

    @classmethod
    def count_sources_clasified_by_term(cls, uuid, level=0):
        """

        """
        if uuid:
            term = Term.query.filter_by(uuid=uuid).first()
            if term:
                aggs = dict()
                aggs[str(term.uuid)] = {
                    "filter": {
                        "term": {
                            "relations.uuid": term.uuid
                            }
                        }
                    }
                query_body = {
                    "aggs": aggs
                    }
                result = SourceSearch.from_dict(query_body).execute()

                children = []
                if level > 0:
                    children = cls._count_term_children(term, level, 1)
                    children.sort(key=lambda k: int(k['count']), reverse=True)
                res = dict(
                    name=term.name,
                    uuid=str(term.uuid),
                    count=str(result.aggregations[str(term.uuid)]["doc_count"]),
                    children=children
                    )
                return result_wrapper(res)
        return None

    @classmethod
    def _count_term_children(cls, term, level_to_reach, current_level):
        # TODO: esto seguramente tiene una mejor manera de hacerse con la query de elasticsearch...
        aggs = dict()
        children = Term.query.filter_by(parent_id=term.id).all()
        for child in children:
            # terms.append(child.uuid)
            aggs[str(child.uuid)] = {
                "filter": {
                    "term": {
                        "relations.uuid": child.uuid
                        }
                    }
                }
        query_body = {
            "aggs": aggs
            }
        result = SourceSearch.from_dict(query_body).execute()
        res = []
        for child in children:
            children = []
            if level_to_reach > current_level:
                children = cls._count_term_children(child, level_to_reach, current_level + 1)
                children.sort(key=lambda k: int(k['count']), reverse=True)
            res.append(
                dict(
                    name=child.name,
                    uuid=str(child.uuid),
                    count=str(result.aggregations[str(child.uuid)]["doc_count"]),
                    children=children
                    )
                )
        return result_wrapper(res)

    @classmethod
    def get_sources_by_term_uuid(cls, uuid):
        if not uuid:
            raise Exception('Must specify an uuid')

        term = Term.query.filter_by(uuid=uuid).first()

        if not term:
            raise Exception('No term found associated to uuid:{0}'.format(uuid))

            terms_ids = []
            if term:
                try:

                    Terms.get_term_tree_list(term, terms_ids)

                    sources_ids = db.session.query(TermSources.sources_id).filter(
                        TermSources.term_id.in_(terms_ids)
                        ).all()

                    return Source.query.filter(Source.id.in_(sources_ids)).all()
                except  Exception as e:
                    raise e
        return None

    @classmethod
    def get_sources_count_by_vocabulary(cls, vocabulary_id):
        # cls.get_term_tree_list(term, terms_ids)
        list_counts = db.session.query(
            Term.identifier, func.count(TermSources.sources_id).label("count")
            ).join(
            TermSources
            ).filter(Term.vocabulary_id == vocabulary_id).order_by(desc('total')).group_by(
            Term.id
            ).all()
        # # print(list_counts)

        return list_counts

    @classmethod
    def _check_source_exist(cls, data):
        """ comprobar que no exista otro Title,ISSN, RNPS o URL igual

            :returns: boolean, Source
        """

        # TODO: Replace this function by Pidstore for sources.
        # esto cambiaria la filosofia un poco, hay que definir diferentes PIDs para los sources,
        # y eso depende del tipo de source, aqui nada mas se estan reflejando los de revistas y
        # lo hace mirando en el data, lo que no es la mejor manera.
        title = data['title'] if 'title' in data else ''
        issn = data['issn'] if 'issn' in data else ''
        rnps = data['rnps'] if 'rnps' in data else ''
        url = data['url'] if 'url' in data else ''

        source = Source.query.filter_by(name=title).first()
        if source:
            return True, source

        result = []
        # sources = Source.query.filter(or_(Source.source_status==SourceStatus.APPROVED,
        # Source.source_status==SourceStatus.TO_REVIEW)).all()
        sources = Source.query.all()

        for item in sources:
            if not issn_is_in_data(item.data, issn, True):
                if not field_is_in_data(item.data, 'rnps', rnps, True):
                    if field_is_in_data(item.data, 'url', url, True):
                        return True, item
                else:
                    return True, item
            else:
                return True, item

        return False, None

    @classmethod
    def insert_new_source(cls, json_data, source_status=SourceStatus.TO_REVIEW, user=None):
        """Insert new Source and an associated SourceVersion
            return [success, message, source]
        """
        # FIXME
        #  TODO: probar with db.session.begin_nested():
        # aqui en este fichero y en otros..
        msg = ''
        source = None
        if not user:
            if not current_user:
                raise Exception('Must be authenticated')
            user_id = current_user.id
        else:
            user_id = user.id

        created_source, msg = SourceRecord.create_or_update(
            None, json_data, dbcommit=True, reindex=False
            )
        return created_source, msg

        # print('user {0}'.format(user_id))
        try:
            # print('try')
            # exist, source = cls._check_source_exist(json_data['data'])
            # print(json_data)
            # valid_data = source_schema.load(json_data)
            valid_data = json_data

            pid = pids.get_pid_by_data(json_data['data'])
            # print(pid)
            if pid:
                # print('pid={0}'.format(pid))
                source = cls.get_source_by_id(uuid=pid.object_uuid)
                # print(source)

                if not source:
                    msg, source = cls._insert_new_source_helper(
                        user_id, user, valid_data, source_status,
                        pid.object_uuid
                        )
                    # raise Exception('pid {0}={1} is associated with object {2}'.format(
                    # pid.pid_type, pid.pid_value,
                    #                                                                    pid.object_uuid))

                if source.source_status is SourceStatus.UNOFFICIAL:
                    msg, source, version = cls.insert_new_source_version(
                        json_data, source.uuid, True, user=user
                        )
                    # raise Exception('Source already exist uuid={0}. Call
                    # insert_new_source_version'.format(source.uuid))

            elif pids.check_data_identifiers(json_data['data']):
                # print('elif pids.check_data_identifiers(json_data):')

                msg, source = cls._insert_new_source_helper(
                    user_id, user, valid_data, source_status
                    )
                msg, source, version = cls.insert_new_source_version(
                    json_data, source.uuid, True, user=user
                    )

        except Exception as e:
            msg = 'ERROR {0} - {1} - Exception: {2}'.format(e, json_data, str(e))

        return msg, source

    @classmethod
    def _insert_new_source_helper(cls, user_id, user, valid_data, source_status, source_uuid=None):
        new_source = Source()
        if source_uuid is not None:
            new_source.uuid = source_uuid
        new_source.name = valid_data['name']
        new_source.source_type = valid_data['source_type']
        new_source.source_status = source_status
        new_source.data = valid_data['data']
        # print(new_source)
        db.session.add(new_source)

        # transactions are taking place but, however, are not written to disk yet...
        # so we can use new_source.id for granting editor permission
        db.session.commit()
        # print(new_source)
        # print('new source')
        try:
            data = valid_data['data']
            data[pids.IROKO_UUID_FIELD] = str(new_source.uuid)
            data['name'] = new_source.name
            data['source_type'] = new_source.source_type.value
            data['source_status'] = new_source.source_status.value
            data['relations'] = cls._get_relations_to_sync(new_source.id)
            cls.grant_source_editor_permission(user_id, new_source.uuid)
            # print('permision')
            SourceRecord.create_or_update(new_source.uuid, data, dbcommit=True, reindex=False)
            # print('index')

            # cls.insert_new_source_version(new_source.data, new_source.uuid, is_current=True,
            # is_flush=False,
            #                               user=user)
            # # print('version')
        except Exception as e:
            Source.query.filter_by(uuid=new_source.uuid).delete()
            db.session.commit()
            raise (e)

        db.session.commit()

        msg = 'New Source created id={0}'.format(new_source.id)
        return msg, new_source

    # TODO: Revisar esto...
    @classmethod
    def set_source_current(cls, data, source) -> Dict[str, Source]:
        # TODO: cuando es current, se actualiza el source record en el indice
        # y se actualizan los identificadores persistentes..
        return "", None
        if not current_user:
            raise Exception('Must be authenticated')

        if not source:
            raise Exception('Source not exist')

        # user_id, source_id, comment, data, created_at, is_current
        source_version = TermSources.query.filter_by(sources_id=source.id).first()
        source_version.is_current = True
        source.data = data
        # cls._fix_update_term_source_relations(source)

        db.session.commit()

        msg = 'Source id={0} is now current'.format(source_version.id)
        return msg, source

    # TODO: this method is much more complex... a lot of things will happend here
    # TODO: aprobar es como cuando es current, se actualiza el source record en el indice
    # y se actualizan los identificadores persistentes..
    @classmethod
    def set_source_approved(cls, source):

        source.source_status = SourceStatus.APPROVED
        db.session.commit()
        return True

    # TODO: revisar esto, no usar
    @classmethod
    def edit_source_version(cls, data, source_version) -> [str, Source, SourceVersion]:
        """ only editors can edit a version, if not approved
         no usar"""
        return "", None
        if source_version.reviewed:
            raise Exception('Sources is already reviewed.')
        source = source_version.source
        source_version.data = data
        if "comment" in data:
            source_version.comment = data["comment"]
        source_version.is_current = source.source_status is not SourceStatus.APPROVED
        if source_version.is_current:
            source.data = data
            # cls._fix_update_term_source_relations(source)
        db.session.commit()
        msg = 'SourceVersion edited id={0}'.format(source_version.id)
        return msg, source, source_version

    @classmethod
    def insert_new_source_version(
        cls, input_data, uuid, is_current=False, is_flush=False, user=None,
        comment='no comment'
        ) -> [str, Source,
              SourceVersion]:
        """Insert new SourceVersion to an existing Source
        """
        msg = ''
        if not user:
            if not current_user:
                raise Exception('Must be authenticated')
            user_id = current_user.id
        else:
            user_id = user.id

        # TODO: usar las clases de marshmallow,en todas las api, o por lo menos decidir....
        # # print(input_data)
        # # version_schema = SourceVersionSchema(exclude=['user_id'])
        # version_data:SourceVersionSchema = source_version_schema.load(input_data, partial=True,
        # ['comment', 'source_id', 'data']],unknown=INCLUDE)
        # # print("###### load #####")
        # user_id, source_id, comment, input_data, created_at, is_current

        source = cls.get_source_by_id(uuid=uuid)
        if not source:
            raise Exception('No Souce !!')

        if is_current:
            for version in source.versions:
                version.is_current = False
            db.session.commit()
        new_source_version = SourceVersion()
        new_source_version.created_at = datetime.now()
        new_source_version.is_current = is_current
        new_source_version.source_id = source.id
        new_source_version.comment = comment
        new_source_version.user_id = user_id
        # print("### new source created")
        db.session.add(new_source_version)
        # print("db.session.add(new_source_version)")
        if is_flush:
            db.session.flush()
            # print("db.session.flush")
        else:
            db.session.commit()
            # print("db.session.commit")
        # print("#### gggggg")
        data = dict(input_data['data'])
        # print("#### gggggg")
        new_source_version.data = data
        # print("#### gggggg")
        if is_current:
            # print("### cls._fix_update_term_source_relations(source)")
            # print(data)
            relations = cls._fix_update_term_source_relations(source, data)
            data['term_sources'] = relations
            # print(data)
            # print("### cls._fix_update_term_source_relations(source)")
            new_source_version.data = data
            source.data = data
        # print("#### gggggg")
        db.session.commit()
        # print("#### gggggg")
        msg = 'New SourceVersion created id={0}'.format(new_source_version.id)
        return msg, source, new_source_version

    @classmethod
    def _fix_update_term_source_relations(cls, source: Source, data):
        """
        The model TermSources map the relations of Source with any term. In source.data[
        term_sources] are all the term ids related to the source, this is done this way to
        simplify the consumer apps and version handling. This function use source.data to sync
        term-source relations, meaning that new relations in source.data will be included in
        TermSource table, and relations in TermSource not present in source.data will be removed.

        also: update the terms in the relations of the source (term_sources),
        this is for institutional data...
        """

        TermSources.query.filter_by(sources_id=source.id).delete()
        # print("delete")
        db.session.commit()
        # print("commit")

        fixed_relations = []
        if "term_sources" in data:
            for ts in data["term_sources"]:
                # print(ts)
                if cls.is_term_editable_by_source(ts):
                    term_data = ts['term']
                    term = None
                    if 'term_id' in ts and ts['term_id'] != '':
                        try:
                            term_id = int(ts['term_id'])
                            term = Term.query.filter_by(id=term_id).first()
                            # print('****** EDIT')
                            # print(term)
                            if term:
                                msg, term = Terms.edit_term(term.uuid, term_data)
                                # print(msg)
                        except Exception as e:
                            term = None
                    elif 'name' in term_data:
                        term = Term.query.filter_by(identifier=term_data['name']).first()
                        # print('****** NEW')
                        # print(term)
                        if term is None:
                            msg, term = Terms.new_term(term_data)
                            # print(msg)
                        else:
                            msg, term = Terms.edit_term(term.uuid, term_data)
                            # print(msg)
                    if term:
                        fixed_relations.append(
                            dict(
                                source_id=source.id,
                                term_id=term.id,
                                data=ts['data']
                                )
                            )
                else:
                    fixed_relations.append(dict(ts))
                    # ts = term_schema.dump(term)
        # print(fixed_relations)

        real_relations = []
        for f_relation in fixed_relations:
            # # print(f_relation)
            real_term = Term.query.filter_by(id=f_relation['term_id']).first()
            if real_term is not None:
                existing_relation = TermSources.query.filter_by(
                    sources_id=source.id, term_id=real_term.id
                    ).first()
                if existing_relation is None:
                    new_relation = TermSources()
                    # # print("new")
                    new_relation.sources_id = source.id
                    new_relation.term_id = real_term.id
                    new_relation.data = f_relation['data']
                    db.session.add(new_relation)
                    real_relations.append(
                        dict(
                            source_id=source.id,
                            term_id=real_term.id,
                            data=f_relation['data']
                            )
                        )
                    # print("append ")
        db.session.commit()
        return real_relations

    @classmethod
    def is_term_editable_by_source(cls, relation):
        # TODO: esto es un parche... es para actualizar los datos de los terminos en la relacion
        # pero al hacerlo de esta manera en realidad se permite que se actualice cualquier cosa...
        # habria que filtrar por vocabulario o algo por el estilo...

        if 'term' in relation:
            data = relation['term']
            if 'vocabulary_id' in data:
                vid = data['vocabulary_id']
                return vid == IrokoVocabularyIdentifiers.CUBAN_INTITUTIONS.value or \
                       IrokoVocabularyIdentifiers.EXTRA_INSTITUTIONS.value
        return False

    @classmethod
    def add_term_relations(cls, uuid, terms):
        """
        add term_source relations to data and current_version data.
        and sync relations...
        """
        source = Source.query.filter_by(uuid=uuid)
        if source:
            current_version = SourceVersion.query.filter_by(is_current=True).first()
            data = dict(source.data)
            relations = []
            if "term_sources" in data:
                for rel in data["term_sources"]:
                    if 'term_id' in rel and rel['term_id'] != '':
                        to_add = True
                        for term in terms:
                            if str(term.id) == rel['term_id']:
                                to_add = False
                        if to_add:
                            relations.append(rel)
                for term in terms:
                    relations.append(
                        dict(
                            source_id=source.id,
                            term_id=term.id,
                            data=dict()
                            )
                        )
                data['term_sources'] = relations
                relations = cls._fix_update_term_source_relations(source, data)
                data['term_sources'] = relations
                if current_version:
                    current_version.data = data
                source.data = data
                # print(data)
                # print(source.data)
                db.session.commit()
