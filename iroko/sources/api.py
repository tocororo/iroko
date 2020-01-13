
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
from iroko.sources.permissions import ObjectSourceEditor, ObjectSourceGestor

from iroko.sources.utils import _load_terms_tree,sync_term_source_with_data
# from iroko.sources.permissions import grant_source_editor_permission

from iroko.sources.journals.utils import issn_is_in_data, field_is_in_data, _no_params, _filter_data_args, _filter_extra_args

class Sources:
    """API for manipulation of Sources
    Considering SourceVersion: meanining this class use Source and SourceVersion model.
    """

    @classmethod
    def get_source_by_id(cls, id=None, uuid= None):
        if id is not None:
            return Source.query.filter_by(id=id).first()
        if uuid is not None:
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
    def insert_new_source(cls, user, json_data) -> Dict[Dict[bool, str], Source]:
        """Insert new Source and an associated SourceVersion
            return [success, message, source]
        """

        #FIXME
        user_id = 1

        msg = ''


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
                db.session.commit()

                # if current_user:
                #     grant_source_editor_permission(current_user, source)

                cls.insert_new_source_version(user, new_source.data, new_source.id, True)

                msg = 'New Source created id={0}'.format(new_source.id)
                return dict(True, msg), new_source
            else:
                msg = str(errors)
                return dict(False, msg), None



    @classmethod
    def insert_new_source_version(cls, user, data, source_uuid, is_current:bool):
        """Insert new SourceVersion to an existing Source
        """

        #FIXME
        user_id = 1

        msg = ''

        source = Source.query.filter_by(uuid=source_uuid).first()

        if not source:
            msg = 'Source not exist: uuid={0}'
            return msg, None
        else:
            # user_id, source_id, comment, data, created_at, is_current
            new_source_version = SourceVersion()
            new_source_version.data = data
            new_source_version.created_at = datetime.now()
            new_source_version.is_current = is_current
            new_source_version.source_id = source.id
            new_source_version.comment = data["comment"] if "comment" in data else ""
            new_source_version.user_id = user_id

            if is_current:
                source.data = data
                sync_term_source_with_data(source)

            db.session.add(new_source_version)
            db.session.commit()

            msg = 'New SourceVersion created id={0}'.format(new_source_version.id)
            return msg, new_source_version

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
                if not source.data:
                    source.data = {'editor':[user.id]}
                else:                    
                    source.data['editor'].append(user.id)
                    
                db.session.commit()
                msg = 'Editor Permission granted over {0}'.format(source.name)
                done = True
            
        except Exception as e:
            msg = str(e)
            print(str(e))
        
        return msg, done

