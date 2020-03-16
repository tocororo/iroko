from typing import Dict
from flask_babelex import lazy_gettext as _
from flask_login import current_user
from sqlalchemy import and_, or_, not_, desc, asc
from iroko.sources.models import Source, TermSources, SourceStatus, SourceType, SourceVersion
from iroko.taxonomy.models import Term
from iroko.sources.marshmallow.source import source_schema, source_version_schema, SourceVersionSchema, EXCLUDE, INCLUDE
from invenio_db import db
from datetime import datetime
from invenio_access import Permission
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from iroko.sources.permissions import ObjectSourceEditor, ObjectSourceGestor, is_current_user_source_admin
from invenio_access.utils import get_identity
from iroko.sources.utils import _load_terms_tree, _load_terms_tree_by_uuid, sync_term_source_with_data
from sqlalchemy_utils.types import UUIDType
from iroko.sources.journals.utils import issn_is_in_data, field_is_in_data, _no_params, _filter_data_args, _filter_extra_args
from iroko.taxonomy.api import Terms
from sqlalchemy import func, desc

from invenio_records.api import Record
from invenio_indexer.api import RecordIndexer
from invenio_jsonschemas import current_jsonschemas
from uuid import uuid4
from elasticsearch.exceptions import NotFoundError
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.resolver import Resolver

import iroko.pidstore.fetchers as iroko_fetchers
import iroko.pidstore.minters as iroko_minters
import iroko.pidstore.providers as iroko_providers

from iroko.sources.search import SourceSearch
from invenio_rest.serializer import result_wrapper

from flask import jsonify

from flask import current_app

from elasticsearch_dsl.connections import connections

from elasticsearch_dsl import Search, Q


class IrokoSource (Record):

    minter = iroko_minters.iroko_source_uuid_minter
    fetcher = iroko_fetchers.iroko_source_uuid_fetcher
    provider = iroko_providers.IrokoSourceUUIDProvider

    source_minter = iroko_minters.iroko_source_source_record_minter
    source_fetcher = iroko_fetchers.iroko_source_source_record_fetcher
    source_provider = iroko_providers.IrokoSourceSourceRecordProvider

    object_type = 'rec'

    pid_uuid_field = 'id'
    _schema = "sources/source-v1.0.0.json"

            
    @classmethod
    def create_or_update(cls, data, id_=None, dbcommit=False, reindex=False, source_uuid=None, **kwargs):
        """Create or update IrokoRecord."""

        if source_uuid:
            source = cls.get_source_by_pid(source_uuid, with_deleted=False)
            if source:
                # merged_data = cls._merge_uri(data, record)
                source.update(data, dbcommit=dbcommit, reindex=reindex)
                return source, 'updated'
        else:
            source = cls.get_record_by_data(data)
            if source:
                print("!AAAAAA")

                source.update(data, dbcommit=dbcommit, reindex=reindex)
                return source, 'updated'
            created_source = cls.create(data, id_=None, dbcommit=dbcommit, reindex=reindex)
            return created_source, 'created'

    @classmethod
    def create(cls, data, id_=None, dbcommit=False, reindex=False, **kwargs):
        """Create a new SourceRecord."""
        data['$schema'] = current_jsonschemas.path_to_url(cls._schema)
        assert cls.minter
        assert not data.get(cls.pid_uuid_field)
        if not id_:
            id_ = uuid4()
        cls.minter(id_, data)
        cls.source_minter(id_, data)
        source = super(IrokoSource, cls).create(data=data, id_=id_, **kwargs)
        if dbcommit:
            source.dbcommit(reindex)
        return source

    @classmethod
    def delete( cls, data, vendor=None, delindex=True, force=False):
        """Delete a IrokoRecord record."""
        assert data.get(cls.pid_uuid_field)
        pid = data.get(cls.pid_uuid_field)
        source = cls.get_source_by_pid(pid, with_deleted=False)
        pid.delete()
        result = source.delete(force=force)
        if delindex:
            try:
                RecordIndexer().delete(source)
            except NotFoundError:
                pass
        return result

    @classmethod
    def get_source_by_pid(cls, pid, with_deleted=False):
        assert cls.provider
        resolver = Resolver(
            pid_type=cls.provider.pid_type,
            object_type=cls.object_type,
            getter=cls.get_record,
        )
        try:
            persistent_identifier, source = resolver.resolve(str(pid))
            return source
            # return super(IrokoRecord, cls).get_record(
            #     persistent_identifier.object_uuid, with_deleted=with_deleted
            # )
        except PIDDoesNotExistError:
            return None

    @classmethod
    def get_record_by_data(cls, data):
        # depending of the providers this method can be more complex, meaning using other external PIDs like url or doi
        assert cls.source_provider
        resolver = Resolver(
            pid_type=cls.source_provider.pid_type,
            object_type=cls.object_type,
            getter=cls.get_record,
        )
        try:
            pid = cls.source_provider.get_pid_from_data(data=data)
            persistent_identifier, record = resolver.resolve(str(pid))
            return record
            # return super(IrokoRecord, cls).get_record(
            #     persistent_identifier.object_uuid, with_deleted=with_deleted
            # )
        except PIDDoesNotExistError:
            return None

    def update(self, data, dbcommit=False, reindex=False):
        """Update data for record."""
        super(IrokoSource, self).update(data)
        super(IrokoSource, self).commit()
        if dbcommit:
            self.dbcommit(reindex)
        return self

    def dbcommit(self, reindex=False, forceindex=False):
        """Commit changes to db."""
        db.session.commit()
        if reindex:
            self.reindex(forceindex=forceindex)

    def reindex(self, forceindex=False):
        """Reindex record."""
        if forceindex:
            RecordIndexer(version_type="external_gte").index(self)
        else:
            RecordIndexer().index(self)

class Sources:
    """API for manipulation of Sources
    Considering SourceVersion: meanining this class use Source and SourceVersion model.
    """

    @classmethod
    def sync_source_index(cls):
        """
        insertar/actualizar todos los Sources (SqlAlchemy) como IrokoSource (Invenio Record)
        """
        sources = Source.query.all()
        for source in sources:
            data = source.data
            if not data:
                data = dict()
            data['source_uuid']= str(source.uuid)
            data['name']= source.name
            data['source_type']= source.source_type.value
            data['source_status']= source.source_status.value
            data['relations']= cls._get_relations_to_sync(source.id)
            # TODO: add identifiers
            ids = []
            if 'issn' in data and 'p' in data['issn']:
                ids.append(dict(idtype='issn', value=data['issn']['p']))
            if 'issn' in data and 'e' in data['issn']:
                ids.append(dict(idtype='issn', value=data['issn']['e']))
            if 'issn' in data and 'l' in data['issn']:
                ids.append(dict(idtype='issn', value=data['issn']['']))
            if 'rnps' in data and 'p' in data['rnps']:
                ids.append(dict(idtype='rnps', value=data['rnps']['p']))
            if 'rnps' in data and 'e' in data['rnps']:
                ids.append(dict(idtype='ernps', value=data['rnps']['e']))
            if 'url' in data:
                ids.append(dict(idtype='url', value=data['url']))
            if 'oai' in data:
                ids.append(dict(idtype='oai', value=data['oai']))
            data['identifiers'] = ids
            src, status = IrokoSource.create_or_update(
                            data, dbcommit=True, reindex=True)

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
    def get_sources_list_x_status(cls, status='all', ordered_by_date=False, term_uuid=None):

        query = db.session.query(Source)

        if status is not 'all':
            query = query.filter(Source.source_status==status.upper())
        
        if term_uuid:
            msg, term = Terms.get_term(term_uuid)
            if term:
                terms_ids = []
                Terms.get_term_tree_list(term, terms_ids)                
                query = query.join(TermSources).filter(TermSources.term_id.in_(terms_ids))

        if ordered_by_date:
            query = query.join(SourceVersion).filter(SourceVersion.is_current==True).order_by(SourceVersion.created_at.desc())
        
        return list(map(lambda x: x, query.all()))        
        

    @classmethod
    def get_sources_id_list(cls):
        #ids = list(map(lambda x: int(x.id), session.query(Source.id).filter(Source.DDDDDD==trigger).all()))
        return list(map(lambda x: int(x.id), db.session.query(Source.id).filter(Source.source_status==SourceStatus.APPROVED).all()))

    @classmethod
    def get_source_by_id(cls, id=None, uuid= None):
        if id is not None:
            return Source.query.filter_by(id=id).first()
        if uuid is not None:
            #uuid = UUIDType(uuid)
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
                aggs[str(term.uuid)]= {
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
                    name= term.name,
                    uuid= str(term.uuid),
                    count= str(result.aggregations[str(term.uuid)]["doc_count"]),
                    children= children
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
            aggs[str(child.uuid)]= {
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
                children = cls._count_term_children(child ,level_to_reach, current_level+1)
                children.sort(key=lambda k: int(k['count']), reverse=True)
            res.append(dict(
                name= child.name,
                uuid= str(child.uuid),
                count= str(result.aggregations[str(child.uuid)]["doc_count"]),
                children= children
            ))
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

                    sources_ids = db.session.query(TermSources.sources_id).filter(TermSources.term_id.in_(terms_ids)).all()

                    return Source.query.filter(Source.id.in_(sources_ids)).all()
                except  Exception as e:
                    raise e
        return None

    @classmethod
    def get_sources_count_by_vocabulary(cls, term_id):
        #cls.get_term_tree_list(term, terms_ids)
        list_counts = db.session.query(Term.name, func.count(TermSources.sources_id).label("count")).join(TermSources).filter(Term.vocabulary_id==vocabulary_id).order_by(desc('total')).group_by(Term.id).all()
        #print(list_counts)

        return list_counts

    @classmethod
    def _check_source_exist(cls, data):
        """ comprobar que no exista otro Title,ISSN, RNPS o URL igual

            :returns: boolean, Source
        """
        # TODO: Replace this function by Pidstore for sources.
        # esto cambiaria la filosofia un poco, hay que definir diferentes PIDs para los sources, y eso depende del tipo de source, aqui nada mas se estan reflejando los de revistas y lo hace mirando en el data, lo que no es la mejor manera.
        title = data['title'] if 'title' in data else ''
        issn = data['issn'] if 'issn' in data else ''
        rnps = data['rnps'] if 'rnps' in data else ''
        url = data['url'] if 'url' in data else ''

        source = Source.query.filter_by(name=title).first()
        if source:
            return True, source

        result = []
        #sources = Source.query.filter(or_(Source.source_status==SourceStatus.APPROVED, Source.source_status==SourceStatus.TO_REVIEW)).all()
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


#  TODO: probar with db.session.begin_nested():
# aqui en este fichero y en otros..

    @classmethod
    def insert_new_source(cls, json_data) -> Dict[Dict[bool, str], Source]:
        """Insert new Source and an associated SourceVersion
            return [success, message, source]
        """
        #FIXME

        if not current_user:
            raise Exception('Must be authenticated')
        try:
            exist, source = cls._check_source_exist(json_data['data'])

            if exist:
                if source.source_status is SourceStatus.UNOFFICIAL:
                    return cls.insert_new_source_version(json_data, source.uuid, True)

                msg = 'Source already exist id={0}. Call insert_new_source_version'.format(source.id)
                #return dict(False, msg), None
                raise Exception(msg)

            valid_data = source_schema.load(json_data)

            new_source = Source()
            new_source.name = valid_data['name']
            new_source.source_type = valid_data['source_type']
            new_source.source_status = SourceStatus.TO_REVIEW
            new_source.data = valid_data['data']
            # print(new_source)
            db.session.add(new_source)

            #transactions are taking place but, however, are not written to disk yet...
            #so we can use new_source.id for granting editor permission
            db.session.flush()
            cls.grant_source_editor_permission(current_user.id, new_source.uuid)
            cls.insert_new_source_version(new_source.data, new_source.id, True, is_flush=True)

            db.session.commit()

            msg = 'New Source created id={0}'.format(new_source.id)
            done = True

        except Exception as e:
            msg = 'ERROR {0} - {1}'.format(e, json_data)
            new_source = None
            done = False
        finally:
            return dict(done, msg), new_source

    # TODO: Revisar esto...
    @classmethod
    def set_source_current(cls, data, source) -> Dict[str, Source]:
        if not current_user:
            raise Exception('Must be authenticated')

        if not source:
            raise Exception('Source not exist')

        # user_id, source_id, comment, data, created_at, is_current
        source_version = TermSources.query.filter_by(sources_id=source.id).first()
        source_version.is_current = True
        source.data = data
        sync_term_source_with_data(source)

        db.session.commit()

        msg = 'Source id={0} is now current'.format(source_version.id)
        return msg, source

    @classmethod
    def set_source_approved(cls, source):
        source.source_status = SourceStatus.APPROVED
        db.session.commit()
        return True

    # TODO: revisar esto, no usar
    @classmethod
    def edit_source_version(data, source_version) -> [str, Source, SourceVersion]:
        """ only editors can edit a version, if not approved """
        if source_version.reviewed:
            raise Exception('Sources is already reviewed.')
        source = source_version.source
        source_version.data = data
        if "comment" in data:
            source_version.comment = data["comment"]
        source_version.is_current = source.source_status is not SourceStatus.APPROVED
        if source_version.is_current:
            source.data = data
            sync_term_source_with_data(source)
        db.session.commit()
        msg = 'SourceVersion edited id={0}'.format(source_version.id)
        return msg, source, source_version

    @classmethod
    def insert_new_source_version(cls, input_data, source, is_current:bool, is_flush=False) -> [str, Source, SourceVersion]:
        """Insert new SourceVersion to an existing Source
        """

        msg = ''
        if not current_user:
            raise Exception('Must be authenticated')
        if not source:
            raise Exception('No Souce !!')

        # TODO: usar las clases de marshmallow,en todas las api, o por lo menos decidir....
        # print(input_data)
        # # version_schema = SourceVersionSchema(exclude=['user_id'])
        # version_data:SourceVersionSchema = source_version_schema.load(input_data, partial=True, ['comment', 'source_id', 'data']],unknown=INCLUDE)
        # print("###### load #####")
        # user_id, source_id, comment, input_data, created_at, is_current
        if is_current:
            for version in source.versions:
                version.is_current = False
            db.session.commit()
        new_source_version = SourceVersion()
        new_source_version.data = input_data['data']
        new_source_version.created_at = datetime.now()
        new_source_version.is_current = is_current
        new_source_version.source_id = source.id
        new_source_version.comment = input_data['comment']
        new_source_version.user_id = current_user.id
        print("### new source created")
        db.session.add(new_source_version)
        print("db.session.add(new_source_version)")
        if is_flush:
            db.session.flush()
            print("db.session.flush")
        else:
            db.session.commit()
            print("db.session.commit")

        if is_current:
            data = dict(input_data['data'])
            source.data = data
            db.session.commit()
            sync_term_source_with_data(source)
            print("### sync_term_source_with_data(source)")


        msg = 'New SourceVersion created id={0}'.format(new_source_version.id)
        return msg, source, new_source_version

    @classmethod
    def grant_source_editor_permission(cls, user_id, source_uuid, is_flush=True) -> Dict[str, bool]:
        done = False
        msg = ''
        try:
            #source = Source.query.filter_by(id=source_id).first()
            # if not source:
            #     msg = 'source not found'

            user = User.query.filter_by(id=user_id)
            if not user:
                msg = 'User not found'
            else:
                db.session.add(ActionUsers.allow(ObjectSourceEditor(source_uuid), user=user))
                if is_flush:
                    db.session.flush()
                else:
                    db.session.commit()
                msg = 'Source Editor Permission granted '
                done = True

        except Exception as e:
            msg = str(e)
            print(str(e))

        return msg, done

    @classmethod
    def get_sources_from_editor_current_user(cls, status='all')-> Dict[str, list]:
        """
            param status: 'all', 'approved', 'to_review', 'unofficial' """


        sources = cls.get_arguments_for_source_from_action(current_user, 'source_editor_actions')

        if not status == 'all':
            sources_directly = db.session.query(Source).filter(Source.uuid.in_(sources), Source.source_status==status.upper()).all()
        else:
            sources_directly = db.session.query(Source).filter(Source.uuid.in_(sources)).all()

        if sources_directly:
            return 'ok', sources_directly

        return 'none', []

    @classmethod
    def get_sources_from_gestor_current_user(cls, status='all')-> Dict[str, list]:
        """
            param status: 'all', 'approved', 'to_review', 'unofficial'
        """

        if is_current_user_source_admin():
            return 'ok', Sources.get_sources_list_x_status(status)

        sources_ids_directly = cls.get_arguments_for_source_from_action(current_user, 'source_gestor_actions')
        if not status == 'all':
            sources_directly = db.session.query(Source).filter(Source.uuid.in_(sources_ids_directly), Source.source_status==status.upper()).all()
        else:
            sources_directly = db.session.query(Source).filter(Source.uuid.in_(sources_ids_directly)).all()

        sources_by_term = []
        terms_uuids = cls.get_arguments_for_source_from_action(current_user, 'source_term_gestor_actions')

        if terms_uuids:
            all_terms = _load_terms_tree_by_uuid(terms_uuids)
            if not status == 'all':
                sources_by_term = db.session.query(Source).join(TermSources, Term).filter(Term.uuid.in_(all_terms), Source.source_status==status.upper()).all()
            else:
                sources_by_term = db.session.query(Source).join(TermSources, Term).filter(Term.uuid.in_(all_terms)).all()

        if sources_directly or sources_by_term:
            return 'ok', sources_directly+sources_by_term

        return 'none', []

    @classmethod
    def get_userids_for_source_from_action(cls, paction, p_argument=None):

        if p_argument:
            user_ids = list(map(lambda x: x.user.id, db.session.query(ActionUsers).filter_by(argument=str(p_argument),exclude=False,action=paction).all()))
        else:
            user_ids = list(map(lambda x: x.user.id, db.session.query(ActionUsers).filter_by(exclude=False,action=paction).all()))

        return user_ids

    @classmethod
    def get_arguments_for_source_from_action(cls, puser, paction):

        arguments = list(map(lambda x: x.argument, db.session.query(ActionUsers).filter_by(user=puser,exclude=False,action=paction).all()))

        return arguments

    @classmethod
    def get_user_ids_source_editor(cls, uuid) -> Dict[str, list]:
        #TODO validate uuid
        gestors = cls.get_userids_for_source_from_action('source_editor_actions', uuid)
        if gestors:
            return 'ok', gestors

        return 'error', []

    @classmethod
    def get_user_ids_source_gestor(cls, uuid) -> Dict[str, list]:
        #TODO validate uuid
        gestors = cls.get_userids_for_source_from_action('source_gestor_actions', uuid)

        if gestors:
            return 'ok', gestors

        source = Sources.get_source_by_id(uuid=uuid)
        if not source:
            raise Exception('Not source found')

        for term_source in source.term_sources:

            term_gestors = cls.get_userids_for_source_from_action('source_term_gestor_actions', term_source.term.uuid)

            if term_gestors:
                return 'ok', term_gestors

            msg, aux = Terms.get_term_by_id(term_source.term_id)

            while aux.parent_id:
                msg, aux = Terms.get_term_by_id(aux.parent_id)
                term_gestors = cls.get_userids_for_source_from_action('source_term_gestor_actions', aux.uuid)
                if term_gestors:
                    return 'ok', term_gestors

        #para obtener al full_gestor por si no hay alguien mas
        admins = cls.get_userids_for_source_from_action('source_full_gestor_actions')
        if admins:
            return 'ok', admins

        return 'error', []

    @classmethod
    def get_editor_versions_not_reviewed(cls, source):
        # lista las versiones de un source que haya creado un editor, en este caso las del current
        # pero solo las versiones que no han sido revisadas por el gestor, en cuyo caso
        # tendria que simplemente editar la fuente, no la versions y asi agregar nuevas versiones
        #

        versions = SourceVersion.query.filter_by(source_id=source.id, user=current_user, reviewed=False).order_by(desc(SourceVersion.created_at)).all()
        print('versiosn', versions)

        return versions

def get_current_user_source_permissions() -> Dict[str, Dict[str, list]]:
    """
    Checks from ActionUsers if current_user has source_full_gestor_actions,
    if not,
    1- then sources of the terms he has GESTOR permissions over with action source_term_gestor_actions,
    or with source_gestor_actions,
    2- sources he has EDITOR permissions with source_editor_actions
    """

    vocabularies_ids = []
    if is_current_user_source_admin():
        return 'actions', {'source_full_gestor_actions': None}

    actions = ActionUsers.query.filter_by(
        user=current_user,
        exclude=False,
        action='source_term_gestor_actions').all()

    terms = []
    for action in actions:
        terms.append(action.argument)

    all_terms = _load_terms_tree(terms)
    print('----------------tree : ', all_terms)
    sources = TermSources.query.filter(TermSources.term_id.in_(all_terms)).all()

    sources_gestor_ids = []
    for source in sources:
        sources_gestor_ids.append(source.sources_id)

    actions = ActionUsers.query.filter_by(
        user=current_user,
        exclude=False,
        action='source_gestor_actions').all()

    for action in actions:
        if action.argument not in sources_gestor_ids:
            sources_gestor_ids.append(action.argument)

    actions = ActionUsers.query.filter_by(
        user=current_user,
        exclude=False,
        action='source_editor_actions').all()

    sources_editor_ids = []
    for action in actions:
        sources_editor_ids.append(action.argument)


    return 'actions', {'source_gestor_actions':sources_gestor_ids, 'source_editor_actions': sources_editor_ids}

