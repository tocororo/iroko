from invenio_access import action_factory
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 


#creando action
notification_admin_actions = action_factory('notification_admin_actions')

ObjectNotificationEditor = action_factory('notification_editor_actions', parameter=True)
Notification_editor_actions = ObjectNotificationEditor(None)



