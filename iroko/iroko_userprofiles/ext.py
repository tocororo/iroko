# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""User profiles module for Invenio."""

from __future__ import absolute_import, print_function

from .api import current_userprofile
from invenio_userprofiles.ext import InvenioUserProfiles


class IrokoUserProfiles(InvenioUserProfiles):
    """Iroko-UserProfiles extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

        # Register current_profile
        app.context_processor(lambda: dict(
            current_userprofile=current_userprofile))

        app.extensions['invenio-userprofiles'] = self

   
