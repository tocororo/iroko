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
from invenio_access import Permission

curator_permission = Permission(RoleNeed('curator'))

def can_edit_patent_factory(record, *args, **kwargs):
    """Checks if logged user can update or delete patent items.
    """
    def can(self):
        if current_user.is_authenticated and curator_permission.can():
            return True
        return False
    return type('Check', (), {'can': can})()
