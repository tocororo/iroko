from os import path, mkdir, removedirs, listdir
import time

import shutil

from lxml import etree

from sickle import Sickle

from flask import current_app

from iroko.harvester.base import SourceIterator, Formater

from iroko.sources.models import Sources

from iroko.harvester.processors.oai import nsmap

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)


from .formaters import DubliCoreElements

class OaiIterator(SourceIterator):

    def __init__(self, logger, source, init_directory=True,max_retries=3):

        self.logger= logger 
        # eventually, check type?
        self.source = source
        self.formater = DubliCoreElements(None)

        p = current_app.config['HARVESTER_DATA_DIRECTORY']

        self.harvest_dir = path.join(p, str(self.source.id))
        if init_directory and path.exists(self.harvest_dir):
            shutil.rmtree(self.harvest_dir)
        if not path.exists(self.harvest_dir):
            mkdir(self.harvest_dir)

        proxies = {"http": "http://servers-proxy.upr.edu.cu:8080","https": "http://servers-proxy.upr.edu.cu:8080"}

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        args = {'headers':headers,'proxies':proxies,'timeout':15, 'verify':False}
        self.sickle = Sickle(self.source.harvest_endpoint, encoding=None,max_retries=max_retries, **args)
        print('self.sickle')
        
        self.formats = []
        arguments ={}
        items = self.sickle.ListMetadataFormats(**arguments)
        for f in items:
            self.formats.append(f.metadataPrefix)
            print(f.metadataPrefix)


    def __iter__(self):
        self.records_iterator = self.sickle.ListRecords(metadataPrefix=self.formater.metadataPrefix)
        return self

    def __next__(self):
        item = self.records_iterator.next()
        data = self.formater.ProcessItem(item.xml)
        return data

    def get_identifiers(self):
        """retrieve all the identifiers of the source, create a directory structure, and save id.xml for each identified retrieved."""
        iterator = self.sickle.ListIdentifiers(metadataPrefix=self.formater.metadataPrefix)
        count=0
        for item in iterator:
            p = path.join(self.harvest_dir, str(count))
            if path.exists(p):
                shutil.rmtree(p)
            mkdir(p)
            f = open(path.join(p,"id.xml"),"w")
            f.write(item.raw)
            f.close()
            count+=1
        print(count)

    def get_all_metadata(self):
        """using the directory structure, iterate over the source folders and retrieve all the metadata of all records."""
        for item in listdir(self.harvest_dir):
            self.harvest_full_item(item)

    def harvest_full_item(self, item):
        """retrieve all the metadata of an item and save it to files"""
        idpath = path.join(self.harvest_dir, item, "id.xml")
        if path.exists(idpath):
            idxml = etree.parse(idpath, parser=XMLParser)
            id = idxml.find('.//{' + nsmap['oai'] + '}' + 'identifier')
            for f in self.formats:
                arguments ={'identifier': id.text,'metadataPrefix':f}
                print(idxml)
                record = self.sickle.GetRecord(**arguments)
                f = open(path.join(self.harvest_dir, item,f+".xml"),"w")
                f.write(record.raw)
                f.close()
                # valitate metadata format
            time.sleep(3)

    def harvest_relation_resources(self, item):
        """retrieve all the files associated to the record (full texts) based on the relation element in oai_dc schema"""
        dcpath = path.join(self.harvest_dir, item, self.formater.metadataPrefix+".xml")
        print(dcpath)
        if path.exists(dcpath):
            xml = etree.parse(dcpath, parser=XMLParser)
            data = self.formater.ProcessItem(xml)
            print(data['relations'])



