
import enum
from iroko.sources.models import Sources
from iroko.harvester.models import HarvestedItem

class Item:

    format = ''
    raw = ''
    data = {}


class SourceHarvesterMode(enum.Enum):

    FILE_SYSTEM = "ERROR"
    REMOTE = "HARVESTED"


class SourceHarvester(object):
    """An iterator is responsible iterate over the items of a source, the OAI case is the most simple, in other case, is also responsible for discover the iterm before iterate over its"""

    def __init__(self, source: Sources):

        self.source = source

    def identity_source(self):
        """ en oai esto significa identify, metadata formats, es decir, aqui se trata lo que tiene que ver con el source"""
        raise NotImplementedError

    def discover_items(self):
        """descubrir los items que tiene, en el caso de oai es el verbo getIdentifiers"""
        raise NotImplementedError

    def process_items(self):
        """ una vez descubiertos los items (los identificadores en el caso de oai, o las urls en otro caso) aqui se procesan todos los items, es decir se traen los datos y eventualmente se crea un record"""
        raise NotImplementedError



class Formater(object):
    """ A Formater will return a dict given something (xml, html, or something else) """

    def __init__(self):
        self.metadataPrefix = None

    def getMetadataPrefix(self):
        """name of the formater oai_dc, nlm, jats"""
        return self.metadataPrefix

    def ProcessItem(self, item:HarvestedItem):
        """given an item return a dict given an item"""
        raise NotImplementedError
