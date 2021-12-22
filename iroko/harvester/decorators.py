#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
from functools import wraps

from flask_login import current_user
from flask_restful import abort

from iroko.harvester.permissions import harvester_permission


def require_harvester_permission():
    """Decorator to require harvester permission.
    """
    def wrapper(f):
        """Wrap function with oauth require decorator."""

        @wraps(f)
        def decorated(*args, **kwargs):
            """Decorated view."""
            if not current_user.is_authenticated:
                abort(401)
            if not harvester_permission.can():
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return wrapper
