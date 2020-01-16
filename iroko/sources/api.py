
from typing import Dict
from flask_login import current_user
from sqlalchemy import and_, or_, not_
from iroko.sources.models import Source, TermSources, SourceStatus, SourceType, SourceVersion
from iroko.taxonomy.models import Term
from iroko.sources.marshmallow import source_schema
from iroko.sources.journals.marshmallow import journal_schema
from invenio_db import db
from datetime import datetime
from invenio_access import Permission
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from iroko.sources.permissions import ObjectSourceEditor, ObjectSourceGestor, is_current_user_source_admin
from invenio_access.utils import get_identity 
from iroko.sources.utils import _load_terms_tree,sync_term_source_with_data
# from iroko.sources.permissions import grant_source_editor_permission
from sqlalchemy_utils.types import UUIDType
from iroko.sources.journals.utils import issn_is_in_data, field_is_in_data, _no_params, _filter_data_args, _filter_extra_args
from iroko.taxonomy.api import Terms



class Sources:
    """API for manipulation of Sources
    Considering SourceVersion: meanining this class use Source and SourceVersion model.
    """

    @classmethod
    def get_sources_id_list(cls):
        #ids = list(map(lambda x: int(x.id), session.query(Source.id).filter(Source.DDDDDD==trigger).all()))
        return list(map(lambda x: int(x.id), db.session.query(Source.id).all()))

    @classmethod
    def get_source_by_id(cls, id=None, uuid= None):        
        if id is not None:
            return Source.query.filter_by(id=id).first()
        if uuid is not None:
            #uuid = UUIDType(uuid)
            return Source.query.filter_by(uuid=uuid).first()

    @classmethod
    def count_sources(cls):
        return Source.query.count()

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
    def insert_new_source(cls, json_data) -> Dict[Dict[bool, str], Source]:
        """Insert new Source and an associated SourceVersion
            return [success, message, source]
        """

        #FIXME
        
        msg = ''
        if not current_user:
            raise Exception('Must be authenticated')

        exist, source = cls._check_source_exist(json_data['data'])

        if exist:
            msg = 'Source already exist id={0}. Call insert_new_source_version'.format(source.id)
            return dict(False, msg), None
        else:

            valid_data, errors = source_schema.load(json_data)
            if not errors:
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
                cls.grant_source_editor_permission(current_user.id, new_source.id)
                
                db.session.commit()

                # if current_user:
                #     grant_source_editor_permission(current_user, source)

                cls.insert_new_source_version(new_source.data, new_source.id, True)

                msg = 'New Source created id={0}'.format(new_source.id)
                return dict(True, msg), new_source
            else:
                msg = str(errors)
                return dict(False, msg), None



    @classmethod
    def insert_new_source_version(cls, data, source_uuid, is_current:bool) -> [str, Source, SourceVersion]:
        """Insert new SourceVersion to an existing Source
        """

        #FIXME
        msg = ''
        if not current_user:
            raise Exception('Must be authenticated')

        source = Source.query.filter_by(uuid=source_uuid).first()

        if not source:
            raise Exception('Source not exist: uuid={0}')            
        
        # user_id, source_id, comment, data, created_at, is_current
        new_source_version = SourceVersion()
        new_source_version.data = data
        new_source_version.created_at = datetime.now()
        new_source_version.is_current = is_current
        new_source_version.source_id = source.id
        new_source_version.comment = data["comment"] if "comment" in data else ""            
        new_source_version.user_id = current_user.id

        if is_current:
            source.data = data
            sync_term_source_with_data(source)

        db.session.add(new_source_version)
        db.session.commit()

        msg = 'New SourceVersion created id={0}'.format(new_source_version.id)
        return msg, source, new_source_version

    @classmethod
    def grant_source_editor_permission(cls, user_id, source_id) -> Dict[str, bool]:
        done = False
        msg = ''
        try:  
            source = Source.query.filter_by(id=source_id).first()
            user = User.query.filter_by(id=user_id)
            if not source:
                msg = 'source not found'
            elif not user:
                msg = 'User not found'
            else:
                db.session.add(ActionUsers.allow(ObjectSourceEditor(source.id), user=user))                     
                db.session.commit()
                msg = 'Source Editor Permission granted over {0}'.format(source.name)
                done = True
            
        except Exception as e:
            msg = str(e)
            print(str(e))
        
        return msg, done
    
    @classmethod
    def check_user_source_editor_permission(cls, user_id, vocabulary_id)-> Dict[str, bool]:
        done = False
        msg = ''
        try:
            if is_current_user_source_admin():
                done = True
            else:
                source = Source.query.filter_by(id=vocabulary_id).first()
                user = User.query.filter_by(id=user_id)
                user_identity = get_identity(user)

                permission = Permission(ObjectSourceGestor(source.id))
                done = permission.allows(user_identity)
                if not done:
                    permission = Permission(ObjectSourceEditor(source.id))
                    done = permission.allows(user_identity)
            pass
        except Exception as e:
            msg = str(e)
            print(str(e))
        
        return msg, done

    @classmethod
    def get_sources_from_editor_current_user(cls)-> Dict[str, list]:
        
        sources = get_arguments_for_source_from_action(current_user, 'source_editor_actions')
        if sources:
            return 'ok', sources
        
        return 'none', []
    
    @classmethod
    def get_sources_from_gestor_current_user(cls)-> Dict[str, list]:
        
        if is_current_user_source_admin():
            return 'ok', Sources.get_sources_id_list()
        
        sources_directly = get_arguments_for_source_from_action(current_user, 'source_gestor_actions')
       
        sources_by_term = []
        terms_ids = get_arguments_for_source_from_action(current_user, 'source_term_gestor_actions')
        if terms_ids:
            all_terms = _load_terms_tree(terms_ids)
            sources_by_term = list(map(lambda x: int(x.id), db.session.query(Source.id).join(TermSources).filter(TermSources.term_id.in_(all_terms)).all()))

        sources = []
        if sources_directly:
            sources.append(sources_directly)
        if sources_by_term:
            sources.append(sources_by_term)
        
        if sources:
            return 'ok', sources
        
        return 'none', []
        

        

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



def get_user_ids_source_gestor(uuid) -> Dict[str, list]:
    #TODO validate uuid
    gestors = get_userids_for_source_from_action('source_gestor_actions', uuid)
    if gestors:
        return 'ok', gestors
    
    source = Sources.get_source_by_id(uuid=uuid)
    
    for term_source in source.terms:
        
        term_gestors = get_userids_for_source_from_action('source_term_gestor_actions', term_source.term_id)
        
        if term_gestors:
            return 'ok', term_gestors
        
        msg, aux = Terms.get_term_by_id(term_source.term_id)
        
        while aux.parent_id:
            print('parent')
            print(aux.parent_id)
            msg, aux = Terms.get_term_by_id(aux.parent_id)
            term_gestors = get_userids_for_source_from_action('source_term_gestor_actions', aux.id)
            if term_gestors:
                return 'ok', term_gestors
    
    #para obtener al full_gestor por si no hay alguien mas
    admins = get_userids_for_source_from_action('source_full_gestor_actions')
    if admins:
        return 'ok', admins

    return 'error', []
    


def get_userids_for_source_from_action(paction, p_argument=None):
    user_ids = None
    actions = ActionUsers.query.filter_by(
        argument=str(p_argument),
        exclude=False,
        action=paction).all()
    
    if actions:
        user_ids = []
        for action in actions:
            user_ids.append(action.user.id)
    
    return user_ids


def get_arguments_for_source_from_action(puser, paction):
    arguments = None
    actions = ActionUsers.query.filter_by(
        user=puser,
        exclude=False,
        action=paction).all()
    
    if actions:
        arguments = []
        for action in actions:
            if action.argument:
                arguments.append(action.argument)
    
    return arguments