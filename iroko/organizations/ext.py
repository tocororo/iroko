# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.


"""Flask extension for Iroko Organizations."""

from __future__ import absolute_import, print_function

from invenio_files_rest.signals import file_deleted, file_uploaded
from invenio_indexer.signals import before_record_index

from . import indexer
from .cli import organizations
from .tasks import update_record_files_async


class IrokoOrganizations(object):
    """Iroko extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        app.cli.add_command(organizations)
        # self.init_config(app)
        app.extensions['iroko-organizations'] = self
        # self._register_signals(app)


    # def _register_signals(self, app):
    #     """Register signals."""
    #     before_record_index.dynamic_connect(
    #         indexer.indexer_receiver,
    #         sender=app,
    #         index="organizations-organization-v1.0.0")
    #
    #     file_deleted.connect(update_record_files_async, weak=False)
    #     file_uploaded.connect(update_record_files_async, weak=False)
