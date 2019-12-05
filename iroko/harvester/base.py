
import enum
from iroko.sources.models import Source

class Item:

    format = ''
    raw = ''
    data = {}


class SourceHarvesterMode(enum.Enum):

    FILE_SYSTEM = "ERROR"
    REMOTE = "HARVESTED"


class SourceHarvester(object):
    """An iterator is responsible iterate over the items of a source, the OAI case is the most simple, in other case, is also responsible for discover the iterm before iterate over its"""

    def __init__(self, source: Source, work_remote=True, request_wait_time=3):

        self.source = source

    def identity_source(self):
        """ en oai esto significa identify, metadata formats, es decir, aqui se trata lo que tiene que ver con el source"""
        raise NotImplementedError

    def discover_items(self):
        """descubrir los items que tiene, en el caso de oai es el verbo getIdentifiers y posteriormente , se traen los datos, en el caso de oai, esto es traer para cada item todos los metadata formats y guardarlo como ficheros xml en el HARVESTER_DATA_DIRECTORY"""
        raise NotImplementedError

    def process_items(self):
        """ una vez descubiertos los items aqui se procesan y eventualmente se crea un record"""
        raise NotImplementedError


class Formater(object):
    """ A Formater will return a dict given something (xml, html, or something else) """

    def __init__(self):
        self.metadataPrefix = None

    def getMetadataPrefix(self):
        """name of the formater oai_dc, nlm, jats"""
        return self.metadataPrefix

    def ProcessItem(self, item):
        """given an item return a dict given an item"""
        raise NotImplementedError


