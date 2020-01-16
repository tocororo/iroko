from functools import wraps
from flask import Flask, jsonify, request
from iroko.taxonomy.api import is_current_user_taxonomy_admin
from iroko.sources.permissions import is_current_user_source_admin
from flask_login import current_user
from iroko.utils import iroko_json_response, IrokoResponseStatus



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