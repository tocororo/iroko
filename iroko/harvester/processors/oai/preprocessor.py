from os import path, mkdir, removedirs, listdir
import time

import shutil

from lxml import etree

from flask import current_app

from iroko.harvester.base import SourceIterator, Formater


from iroko.sources.models import Sources

from iroko.harvester.processors.oai import nsmap

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)


from .formaters import DubliCoreElements, JournalPublishing

class OaiPreprocessor:

    def __init__(self, logger, source):

        self.logger= logger 
        self.source = source
        p = current_app.config['HARVESTER_DATA_DIRECTORY']
        self.harvest_dir = path.join(p, str(self.source.id))
        
        self.dc = DubliCoreElements(None)
        self.nlm = JournalPublishing(None)
        self.formats = ['marcxml', 'nlm', 'oai_dc','oai_marc', 'rfc1807']

    def process_all_items(self):
        """using the directory structure, iterate over the source folders and retrieve all the metadata of all records."""
        for item in listdir(self.harvest_dir):
            self.process_full_item(item)

    def process_full_item(self, item):
        """retrieve all the metadata of an item and save it to files"""
        idpath = path.join(self.harvest_dir, item, "id.xml")
        if path.exists(idpath):
            dc = self.process_metadata(item, 'oai_dc', self.dc)
            nlm = self.process_metadata(item, 'nlm', self.dc)

    
    def process_metadata(self, item, metadata_format, formater):
        xmlpath = path.join(self.harvest_dir, item, metadata_format + ".xml")
        if path.exists(xmlpath):
            xml = etree.parse(xmlpath, parser=XMLParser)
            return formater.ProcessItem(xml)
    
    def create_record_data(self, dc, nlm):
        data = {}

        data['original_identifier'] = dc['original_identifier']
        data['source'] = self.source.uuid
        
        
        # data['title'] = str(oai_record.metadata['title'])

        # data['keywords'] = oai_record.metadata['subject']
        # data['description'] = str(oai_record.metadata['description'])
        # data['language'] = str(oai_record.metadata['language'])
        # data['publication_date'] = oai_record.metadata['date'][0]
        
        # creators = []
        # for c in oai_record.metadata['creator']:
        #     creators.append({'name': str(c)})
        # data['creators'] = creators

        # ref = []
        # for c in oai_record.metadata['relation']:
        #     ref.append({'raw_reference': str(c)})
        # data['references'] = ref

        # return data