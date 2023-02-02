# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.


"""Flask extension for Iroko Organizations."""

from __future__ import absolute_import, print_function

from iroko.persons.cli import persons


class IrokoPersons(object):
    """Iroko extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        app.cli.add_command(persons)
        # self.init_config(app)
        app.extensions['iroko-persons'] = self
