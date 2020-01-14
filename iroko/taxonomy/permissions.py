from invenio_access import action_factory
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 
from invenio_access import Permission



#creando action
taxonomy_full_editor_actions = action_factory('taxonomy_full_editor_actions')
ObjectVocabularyEditor = action_factory('vocabulary_editor_actions', parameter=True)
vocabulary_editor_actions = ObjectVocabularyEditor(None)


def vocabulary_editor_permission_factory(obj):
    return Permission(ObjectVocabularyEditor(obj['id']))


taxonomy_full_editor_permission = Permission(taxonomy_full_editor_actions)