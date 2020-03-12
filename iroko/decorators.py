from functools import wraps
from flask import Flask, jsonify, request
from iroko.taxonomy.permissions import is_current_user_taxonomy_admin
from iroko.sources.permissions import is_current_user_source_admin
from iroko.notifications.permissions import notification_admin_actions
from flask_login import current_user
from iroko.utils import iroko_json_response, IrokoResponseStatus
from invenio_access.utils import get_identity 
from invenio_access import Permission


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
                'Need to be taxonomy administrator.', 
                None, 
                None
            )
        else:
            return fn(*args, **kwargs)

    return wrapper


def source_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):               
        if not is_current_user_source_admin():
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