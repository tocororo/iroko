#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from flask_login import current_user
from invenio_access import Permission, action_factory
from invenio_access.utils import get_identity

# creando action
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
