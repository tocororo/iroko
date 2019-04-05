from sickle import Sickle

from iroko.modules.harvester.ext import SourceIterator, Formater

from iroko.modules.sources.models import Sources

from .dc.elements import DubliCoreElements

class OaiIterator(SourceIterator):

    def __init__(self, logger, source):
        self.logger= logger 
        # eventually, check type?
        self.source = source

    def __iter__(self):
        sickle = Sickle(self.source.harvest_endpoint, encoding=None)
        # eventually discover formats and decide metadataPrefix argument... 
        self.formater = DubliCoreElements()
        # logger, start iteration.. 
        self.iterator = sickle.ListRecords(metadataPrefix=self.formater.metadataPrefix)
        return self

    def __next__(self):
        # logger, start iteration.. 
        item = self.iterator.next()
        self.formater.ProcessRecord(item)
        print(item.header.identifier)
        return item


