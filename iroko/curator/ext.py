"""Fixtures extension."""

from __future__ import absolute_import, division, print_function



class IrokoCurator(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.cli.add_command(harvester)
        app.extensions['iroko-curator'] = self

