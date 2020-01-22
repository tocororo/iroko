from invenio_access import action_factory
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 
from flask_login import current_user


#creando action
notification_admin_actions = action_factory('notification_admin_actions')

ObjectNotificationViewed = action_factory('notification_viewed_actions', parameter=True)
notification_viewed_actions = ObjectNotificationViewed(None)

def notification_viewed_permission_factory(obj):
    try:
        permission = Permission(notification_admin_actions)
        current_identity = get_identity(current_user)
        if permission.allows(current_identity):
            return permission

    except Exception as e:
        pass

    return Permission(ObjectNotificationViewed(obj['id']))



