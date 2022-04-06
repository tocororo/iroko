# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# Iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Permissions for Iroko."""
from flask_login import current_user
from flask_principal import RoleNeed
from invenio_access import Permission, any_user

curator_permission = Permission(RoleNeed('curator'))

def can_edit_organization_factory(record, *args, **kwargs):
    """Checks if logged user can update or delete its organisation items.

    librarian must have librarian or system_librarian role.
    librarian can only update, delete items of its affiliated library.
    sys_librarian can update, delete any item of its org only.
    """
    def can(self):
        if current_user.is_authenticated and curator_permission.can():
            return True
        return False
    return type('Check', (), {'can': can})()
