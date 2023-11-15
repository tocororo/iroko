# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.


"""Permissions for Iroko Records."""
from invenio_access import Permission, any_user

def files_permission_factory(obj, action=None):
    """Permissions factory for buckets."""
    return Permission(any_user)

