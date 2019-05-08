from os import path, mkdir
import time

import shutil

from lxml import etree

from sickle import Sickle

from flask import current_app

from iroko.harvester.base import SourceHarvester, Formater

from iroko.sources.models import Sources
from iroko.records.api import IrokoRecord

from iroko.harvester.models import Repository, RepositorySet, RepositoryStatus, HarvestedItem, HarvestedItemStatus

from invenio_db import db

from . import nsmap, request_headers
from .formaters import DubliCoreElements, JournalPublishing
from ..errors import IrokoHarvesterError

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)

class OaiHarvester(SourceHarvester):
    """ esta clase maneja todo lo relacionado con el harvesting de un source, llega hasta insertar/actualizar los records, al mismo tiempo, crea una estructura de carpetas donde se almacena todo lo cosechado sin procesar 
    dentro de current_app.config['HARVESTER_DATA_DIRECTORY'] crea una carpeta con el Id del source. 
     con la siguiente forma: 
     [source_id]
        - identify.xml
        - metadata_formats.xml
        - sets.xml
        - [item_id]
            - id.xml
            - metadata_format_1.xml
            - metadata_format_2.xml
            - fulltext_1.ext
            - fulltext_2.ext
    Cuando se cosecha una fuente por primera vez se crea la estructura de carpetas y se almacena en la base de datos lo necesario. 
    Cuando actualiza la cosecha una fuente, o sea cuando ya se ha cosechado otras veces, se modifica la estructura de carpetas si es necesario, si hay que adicionar items, o si cambiaron algunos,etc
    """


    def __init__(self, source: Sources):

        # init_directory=True
        max_retries=3

        self.source = source
        #TODO changeme
        p = current_app.config['HARVESTER_DATA_DIRECTORY']
        # p = 'data/sceiba-data'
        self.harvest_dir = path.join(p, str(self.source.id))

        repo = Repository.query.filter_by(source_id=self.source.id).first()
        if not repo:
            if path.exists(self.harvest_dir):
                raise IrokoHarvesterError(self.harvest_dir + 'exists!!!. Source ' + self.source.name)
            mkdir(self.harvest_dir)
            self.repository = Repository()
            self.repository.source_id = self.source.id
            db.session.add(self.repository)
            db.session.commit()
        else:
            self.repository = repo
            if not path.exists(self.harvest_dir):
                raise IrokoHarvesterError(self.harvest_dir + 'NOT exists!!!. Source ' + self.source.name)

        self.oai_dc = DubliCoreElements()
        self.nlm = JournalPublishing()

        # proxies = {"http": "http://servers-proxy.upr.edu.cu:8080","https": "http://servers-proxy.upr.edu.cu:8080"}

        # args = {'headers':request_headers,'proxies':proxies,'timeout':15, 'verify':False}
        args = {'headers':request_headers,'timeout':15, 'verify':False}
        self.sickle = Sickle(self.source.harvest_endpoint, encoding=None,max_retries=max_retries, **args)


    def identity_source(self):
        try:
            self.get_identify()
            self.get_formats()
            self.get_sets()
            self.repository.status = RepositoryStatus.IDENTIFIED
        except Exception as e:
            self.repository.status = RepositoryStatus.ERROR
            self.repository.error_log = e.__doc__
        finally:
            db.session.commit()


    def discover_items(self):
        try:
            self.get_items()
            self.repository.status = RepositoryStatus.HARVESTED
        except Exception as e:
            self.repository.status = RepositoryStatus.ERROR
            self.repository.error_log = e.__doc__
        finally:
            db.session.commit()


    def process_items(self):
        try:
            self.record_items()
            self.repository.status = RepositoryStatus.RECORDED
        except Exception as e:
            self.repository.status = RepositoryStatus.ERROR
            self.repository.error_log = e.__doc__
        finally:
            # db.session.update(self.repository)
            db.session.commit()


    def _write_file(self, name, content, extra_path=""):
        """helper function, always write to f = open(path.join(self.harvest_dir, extra_path, name),"w")"""

        f = open(path.join(self.harvest_dir, extra_path, name),"w")
        f.write(content)
        f.close()


    def get_identify(self):
        """get_identity"""

        identify = self.sickle.Identify()
        self._write_file("identify.xml", identify.raw)
        self.repository.identifier = identify._identify_dict['repositoryIdentifier']


    def get_formats(self):
        """get_formats"""

        self.formats = []
        arguments ={}
        items = self.sickle.ListMetadataFormats(**arguments)
        self._write_file("metadata_formats.xml", items.oai_response.raw)
        for f in items:
            self.formats.append(f.metadataPrefix)
            # if f.metadataPrefix == 'oai_dc':
            #     self.oai_dc = DubliCoreElements()
            # if f.metadataPrefix == 'nlm':
            #     self.nlm = JournalPublishing()
            # if self.oai_dc is None:
                
                
        self.repository.metadata_formats = self.formats
        # TODO: a medida que se incluyan los otros formatos, lo que tiene que pasar es que si el repo no soporta ninguno de los formatos del harvester entonces es que se manda la excepcion... pero por el momento si no soporta oai_dc, entonces no se puede cosechar
        if 'oai_dc' not in self.formats:
            raise IrokoHarvesterError(" oai_dc is not supported by " \
                    + self.repository.identifier + " Repository : Source ID" + self.source) 


    def get_sets(self):
        """get_sets"""

        arguments ={}
        items = self.sickle.ListSets(**arguments)
        self._write_file("sets.xml", items.oai_response.raw)
        for f in items:
            rset = RepositorySet.query.filter_by(repository_id=self.repository.id,\
                                setSpec=f.setSpec).first()
            if not rset:
                rset = RepositorySet()
                rset.repository_id = self.repository.id
                rset.setSpec = f.setSpec
                rset.setName = f.setName
                db.session.add(rset)


    def get_items(self):
        """retrieve all the identifiers of the source, create a directory structure, and save id.xml for each identified retrieved."""

        iterator = self.sickle.ListIdentifiers(metadataPrefix=self.oai_dc.metadataPrefix)
        for item in iterator:
            harvest_item = HarvestedItem.query.filter_by(repository_id=self.repository.id,\
                                identifier=item.identifier).first()
            try:
                if harvest_item is None:
                    harvest_item = HarvestedItem()
                    harvest_item.repository_id = self.repository.id
                    harvest_item.identifier = item.identifier
                    db.session.add(harvest_item)
                    db.session.commit()
                    p = path.join(self.harvest_dir, str(harvest_item.id))
                    if path.exists(p):
                        raise IrokoHarvesterError(p + 'exists!!!. Source:' + self.source.name + " id:" + harvest_item.id + " " + harvest_item.identifier)
                    mkdir(p)
                if item.deleted:
                    harvest_item.status = HarvestedItemStatus.DELETED
                p = path.join(self.harvest_dir, str(harvest_item.id))

                if not path.exists(p):
                    raise IrokoHarvesterError(p + 'NOT exists!!!. Source:' + self.source.name + " id:" + harvest_item.id + " " + harvest_item.identifier)
                self._write_file("id.xml", item.raw, str(harvest_item.id))
                
                if harvest_item.status != HarvestedItemStatus.DELETED:
                    self._get_all_formats(harvest_item)
                    harvest_item.status = HarvestedItemStatus.HARVESTED
                # TODO: time.sleep(5)
            except Exception as e:
                harvest_item.status = HarvestedItemStatus.ERROR
                harvest_item.error_log = e.__doc__
            finally:
                db.session.commit()


    def _get_all_formats(self, item:HarvestedItem):
        """retrieve all the metadata of an item and save it to files"""

        for f in self.formats:
            arguments ={'identifier': item.identifier,'metadataPrefix':f}
            record = self.sickle.GetRecord(**arguments)
            self._write_file(f+".xml", record.raw, str(item.id))
            # TODO: time.sleep(3)
        # TODO: time.sleep(3)


    def record_items(self):
        """ process all item, create an IrokoRecord and save/update it"""

        items = HarvestedItem.query.filter_by(repository_id=self.repository.id).all()
        for item in items:
            if item.status == HarvestedItemStatus.HARVESTED:
                try:
                    dc = self._process_format(item, self.oai_dc)
                    nlm = None
                    if 'nlm' in self.formats:
                        nlm = self._process_format(item, self.nlm)
                    data = self._crate_iroko_dict(item, dc, nlm)
                    record, status = IrokoRecord.create_or_update(data, dbcommit=True, reindex=True)
                    item.status = HarvestedItemStatus.RECORDED
                    item.record = record.id
                except Exception as e:
                    item.status = HarvestedItemStatus.ERROR
                    item.error_log = e.__doc__


    def _process_format(self, item:HarvestedItem, formater: Formater):

        xmlpath = path.join(self.harvest_dir, str(item.id), formater.getMetadataPrefix()+".xml")
        if not path.exists(xmlpath):
            raise IrokoHarvesterError(xmlpath + 'NOT exists!!!. Source:' + self.source.name + " id:" + item.id + " " + item.identifier)
        xml = etree.parse(xmlpath, parser=XMLParser)
        return formater.ProcessItem(xml)


    def _crate_iroko_dict(self, item:HarvestedItem ,dc , nlm=None):

        data = dc
        if nlm is not None:
            data['contributors'] = nlm['contributors']
        
        data['source'] = str(self.source.uuid)
        
        for s in self.repository.sets:
            if data['setSpec']  == s.setSpec:
                data['spec'] = s.setName
        # aqui iria encontrar los tipos de colaboradores usando nlm...
        # tambien es posible hacer un request de los textos completos usando dc.relations
        return data