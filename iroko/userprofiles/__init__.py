# -*- coding: utf-8 -*-

#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""User profiles module for Invenio."""

from __future__ import absolute_import, print_function

from .api import current_userprofile
from .ext import InvenioUserProfiles
from .models import AnonymousUserProfile, UserProfile
from .version import __version__

__all__ = ('__version__', 'InvenioUserProfiles', 'AnonymousUserProfile',
           'UserProfile', 'current_userprofile')
