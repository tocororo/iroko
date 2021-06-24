#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from functools import wraps

from flask_login import current_user
from invenio_access import Permission
from invenio_access.utils import get_identity

from iroko.notifications.permissions import notification_admin_actions
from iroko.sources.permissions import is_user_sources_admin
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.vocabularies.permissions import is_current_user_taxonomy_admin


def taxonomy_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # if not current_user.is_authenticated:
        #     return iroko_json_response(
        #         IrokoResponseStatus.ERROR,
        #         'Need to be authenticated.',
        #         None,
        #         None
        #     )
        if not is_current_user_taxonomy_admin():
            return iroko_json_response(
                IrokoResponseStatus.ERROR,
                'Need to be vocabularies administrator.',
                None,
                None
            )
        else:
            return fn(*args, **kwargs)

    return wrapper


def source_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not is_user_sources_admin(current_user):
            return iroko_json_response(
                IrokoResponseStatus.ERROR,
                'Need to be source administrator.',
                None,
                None
            )
        else:
            return fn(*args, **kwargs)

    return wrapper


def notification_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        permission = Permission(notification_admin_actions)
        current_identity = get_identity(current_user)
        if not permission.allows(current_identity):
            return iroko_json_response(
                IrokoResponseStatus.ERROR,
                'Need to be source administrator.',
                None,
                None
            )
        else:
            return fn(*args, **kwargs)

    return wrapper
