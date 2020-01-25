from invenio_access import action_factory
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 
from invenio_access import Permission
from flask_login import current_user



#creando action
taxonomy_full_editor_actions = action_factory('taxonomy_full_editor_actions')
ObjectVocabularyEditor = action_factory('vocabulary_editor_actions', parameter=True)
vocabulary_editor_actions = ObjectVocabularyEditor(None)


def vocabulary_editor_permission_factory(obj):
    try:
        permission = Permission(taxonomy_full_editor_actions)
        current_identity = get_identity(current_user)
        if permission.allows(current_identity):
            return permission
    except Exception as e:
        msg = str(e)
    return Permission(ObjectVocabularyEditor(obj['id']))


taxonomy_full_editor_permission = Permission(taxonomy_full_editor_actions)


def is_current_user_taxonomy_admin():

    its = False
    try:
        print('user')
        print(current_user)
        admin = ActionUsers.query.filter_by(
            user=current_user,
            exclude=False,
            action='taxonomy_full_editor_actions').first()

        if admin:
            its = True

    except Exception as e:
        print(str(e))

    return its