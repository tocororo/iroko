#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from functools import wraps

from flask import request, session
from flask_login import current_user


def require_keycloak_auth(
    require_token=False, scopes_required=None,
    render_errors=True
    ):
    """
    """

    def wrapper(f):
        """Wrap function with oauth require decorator."""

        @wraps(f)
        def decorated(*args, **kwargs):
            """Require OAuth 2.0 Authentication."""
            print('------------------------------------------------')
            print('------------------------------------------------')
            print(session)
            print('------------------------------------------------')

            print(current_user)
            print('------------------------------------------------')

            if 'Authorization' in request.headers and request.headers['Authorization'].startswith(
                'Bearer '
                ):
                token = request.headers['Authorization'].split(None, 1)[1].strip()
            if 'access_token' in request.form:
                token = request.form['access_token']
            elif 'access_token' in request.args:
                token = request.args['access_token']
            print(token)
            print('------------------------------------------------')
            print('------------------------------------------------')
            print('------------------------------------------------')
            #
            #
            # if not hasattr(current_user, 'login_via_oauth2'):
            #     if not current_user.is_authenticated:
            #         if allow_anonymous:
            #             return f(*args, **kwargs)
            #         abort(401)
            #     if current_app.config['ACCOUNTS_JWT_ENABLE']:
            #         # Verify the token
            #         current_oauth2server.jwt_verification_factory(
            #             request.headers)
            #     # fully logged in with normal session
            #     return f(*args, **kwargs)
            # else:
            #     # otherwise, try oauth2
            #     return f_oauth_required(*args, **kwargs)

        return decorated

    return wrapper
