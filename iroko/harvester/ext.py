#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Fixtures extension."""

from __future__ import absolute_import, division, print_function

from .cli import harvester


class IrokoHarvester(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.cli.add_command(harvester)
        app.extensions['iroko-harvester'] = self

    # def process_source(self, logger, source_iterator, element_processor):

    #     # logger, start process source with format

    #     source_iterator.logger = logger

    #     for element in source_iterator:
    #         # logger, start process element with format....
    #         record = element_processor.process(element, logger)
