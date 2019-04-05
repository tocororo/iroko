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

    def process_source(self, logger, source_iterator, element_processor):

        # logger, start process source with format
        
        source_iterator.logger = logger

        for element in source_iterator:
            # logger, start process element with format....
            record = element_processor.process(element, logger)



class Formater(object):

    def __init__(self, logger):
        self.logger = logger

    """given an item return a Record"""
    def ProcessItem(self, item):
        raise NotImplementedError



class SourceIterator(object):

    def __init__(self, logger, source):
        self.logger= logger
        # eventually, check type?
        self.source = source


    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError
