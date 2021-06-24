#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Fixtures extension."""

from __future__ import absolute_import, division, print_function


class IrokoTexts(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        # app.cli.add_command(harvester)
        app.extensions['iroko-texts'] = self
