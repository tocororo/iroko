from invenio_access import action_factory
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 



#creando action
ObjectVocabularyEditor = action_factory('vocabulary_editor_actions', parameter=True)
vocabulary_editor_actions = ObjectVocabularyEditor(None)



