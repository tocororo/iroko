

class Item:

    format = ''
    raw = ''
    data = {}
    


class SourceIterator(object):
    """An iterator is responsible iterate over the items of a source, the OAI case is the most simple, in other case, is also responsible for discover the iterm before iterate over its"""

    def __init__(self, logger, source):
        self.logger= logger
        # eventually, check type?
        self.source = source


    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError

class Formater(object):
    """ A Formater will return a dict given something (xml, html, or something else) """
    def __init__(self, logger):
        self.logger = logger

    """given an item return a dict given an item"""
    def ProcessItem(self, item):
        raise NotImplementedError
