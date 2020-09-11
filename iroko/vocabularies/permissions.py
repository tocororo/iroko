from flask_login import current_user
from invenio_access import action_factory, Permission
from invenio_access.models import ActionUsers
from invenio_access.utils import get_identity

#creando action
vocabularies_full_editor_actions = action_factory('vocabularies_full_editor_actions')
ObjectVocabularyEditor = action_factory('vocabulary_editor_actions', parameter=True)
vocabulary_editor_actions = ObjectVocabularyEditor(None)


def vocabulary_editor_permission_factory(obj):
    try:
        permission = Permission(vocabularies_full_editor_actions)
        current_identity = get_identity(current_user)
        if permission.allows(current_identity):
            return permission
    except Exception as e:
        msg = str(e)
    return Permission(ObjectVocabularyEditor(obj['name']))


taxonomy_full_editor_permission = Permission(vocabularies_full_editor_actions)


def is_current_user_taxonomy_admin():

    its = False
    try:
        print('user')
        print(current_user)
        admin = ActionUsers.query.filter_by(
            user=current_user,
            exclude=False,
            action='vocabularies_full_editor_actions').first()

        if admin:
            its = True

    except Exception as e:
        print(str(e))

    return its
