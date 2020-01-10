from invenio_access import action_factory
from invenio_access import Permission
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 


#creando action
vocabulary_editor_actions = action_factory('vocabulary_editor_actions', parameter=True)

#creando permiso, que requiere varias acciones, por ahora solo la anterior
vocabulary_editor_permission = Permission(vocabulary_editor_actions)


def grant_vocabulary_editor_permission(user, vocabulary):
    try:        
        db.session.add(ActionUsers.allow(vocabulary_editor_actions(vocabulary.id, user=user)))
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
        return False


def deny_vocabulary_editor_permission(user, vocabulary):
    try:
        db.session.add(ActionUsers.deny(vocabulary_editor_actions(vocabulary.id, user=user)))
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
        return False


def check_user_vocabulary_editor_permission(user, vocabulary):
    try:
        user_identity = get_identity(user)
        permission = Permission(vocabulary_editor_actions(vocabulary.id))
        return permission.allows(user_identity)
    except Exception as e:
        print(str(e))
        return False