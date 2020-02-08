from os import path, mkdir, listdir

from time import sleep

import traceback

import shutil

from lxml import etree

from sickle import Sickle

from flask import current_app

from iroko.harvester.base import SourceHarvester, Formater

from iroko.sources.models import Source

from iroko.records.api import IrokoRecord

from iroko.harvester.models import HarvestedItem, HarvestedItemStatus, Repository

from invenio_db import db

from iroko.harvester.oai import nsmap, request_headers
from iroko.harvester.oai.formaters import DubliCoreElements, JournalPublishing
from iroko.harvester.errors import IrokoHarvesterError
import iroko.harvester.utils as utils

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


    def __init__(self, source: Source, work_remote=True, request_wait_time=3):

        # init_directory=True
        max_retries=3

        super().__init__(source, work_remote, request_wait_time)
        # self.source = source
        # self.work_remote = work_remote
        # self.request_wait_time = request_wait_time

        p = current_app.config['HARVESTER_DATA_DIRECTORY']
        # p = 'data/sceiba-data'
        self.harvest_dir = path.join(p, str(self.source.id))

        if not path.exists(self.harvest_dir):
            mkdir(self.harvest_dir)

        self.oai_dc = DubliCoreElements()
        self.nlm = JournalPublishing()

        # proxies = {"http": "http://servers-proxy.upr.edu.cu:8080","https": "http://servers-proxy.upr.edu.cu:8080"}
        self.repository = Repository.query.filter_by(source_id=self.source.id).first()
        if not self.repository:
            repository = Repository()
        # args = {'headers':request_headers,'proxies':proxies,'timeout':15, 'verify':False}
        args = {'headers':request_headers,'timeout':15, 'verify':False}
        self.sickle = Sickle(self.repository.harvest_endpoint, encoding=None,max_retries=max_retries, **args)


    def identity_source(self):
        try:
            self.get_identify()
            self.get_formats()
            self.get_sets()
            # TODO: habria que analizar denuevo esto.. falta un status que seria identified.. o ver si esto funciona asi..
            self.repository.status = HarvestedItemStatus.HARVESTED
        except Exception as e:
            self.repository.status = HarvestedItemStatus.ERROR
            self.repository.error_log = traceback.format_exc()
            print('error: identity_source(self):')
        finally:
            db.session.commit()


    def discover_items(self):
        if self.repository.status == HarvestedItemStatus.ERROR:
            raise IrokoHarvesterError('calling discover_items of in a inestable repo. Source.id={0}. Source.repo_status={1}'.format(self.source.id, self.repository.status))
        try:
            self.get_items()
            self.repository.status = HarvestedItemStatus.HARVESTED
        except Exception as e:
            self.repository.status = HarvestedItemStatus.ERROR
            self.repository.error_log = traceback.format_exc()
            print('error: discover_items(self):')
        finally:
            db.session.commit()


    def process_items(self):
        if self.repository.status == HarvestedItemStatus.ERROR:
            raise IrokoHarvesterError('calling process_items of in a inestable repo. Source.id={0}. Source.repo_status={1}'.format(self.source.id, self.repository.status))
        try:
            self.record_items()
            self.repository.status = HarvestedItemStatus.RECORDED
        except Exception as e:
            self.repository.status = HarvestedItemStatus.ERROR
            self.repository.error_log = traceback.format_exc()
            print('error: process_items(self):')
        finally:
            db.session.commit()


    def _write_file(self, name, content, extra_path=""):
        """helper function, always write to f = open(path.join(self.harvest_dir, extra_path, name),"w")"""

        f = open(path.join(self.harvest_dir, extra_path, name),"w")
        f.write(content)
        f.close()


    def _get_xml_from_file(self, name, extra_path=""):
        xmlpath = path.join(self.harvest_dir, extra_path, name)
        if not path.exists(xmlpath):
                raise IrokoHarvesterError('working offline and {0} not exists. Source.id={1}'.format(xmlpath, self.source.id))
        return etree.parse(xmlpath, parser=XMLParser)


    def get_identify(self):
        """get_identity, raise IrokoHarvesterError"""
        if self.work_remote:
            identify = self.sickle.Identify()
            xml = identify.xml
            # identifier = identify._identify_dict['repositoryIdentifier']
        else:
            xml = self._get_xml_from_file("identify.xml")
        identifier = xml.find('.//{' + utils.xmlns.oai_identifier() + '}repositoryIdentifier').text

        if self.repository.identifier is not None and self.repository.identifier != identifier:
            raise IrokoHarvesterError('Different identifiers: {0}!={1}. Source.id={2}. work_remote:{3}'.format(self.repository.identifier, identifier, self.source.id, self.work_remote))

        self.repository.identifier = identifier
        if self.work_remote:
            self._write_file("identify.xml", identify.raw)


    def get_formats(self):
        """get_formats, raise IrokoHarvesterError"""

        self.formats = []
        if self.work_remote:
            arguments ={}
            items = self.sickle.ListMetadataFormats(**arguments)
            for f in items:
                self.formats.append(f.metadataPrefix)
            self._write_file("metadata_formats.xml", items.oai_response.raw)
        else:
            xml = self._get_xml_from_file("metadata_formats.xml")
            self.formats = utils.get_multiple_elements(xml, 'metadataPrefix', xmlns=utils.xmlns.oai())
            print(self.formats)

        self.repository.data = str(self.formats)

        # TODO: a medida que se incluyan los otros formatos, lo que tiene que pasar es que si el repo no soporta ninguno de los formatos del harvester entonces es que se manda la excepcion... pero por el momento si no soporta oai_dc, entonces no se puede cosechar
        if 'oai_dc' not in self.formats:
            raise IrokoHarvesterError(" oai_dc is not supported by Source.id={0} ".format(self.source.id))


    def get_sets(self):
        """get_sets"""

        sets = []
        if self.work_remote:
            arguments ={}
            items = self.sickle.ListSets(**arguments)
            self._write_file("sets.xml", items.oai_response.raw)
            rsets = []
            for s in items:
                rsets.append( { s.setSpec: s.setName } )
            if not self.repository.data:
                self.repository.data = {}
            self.repository.data['sets'] = rsets
        else:
            xml = self._get_xml_from_file("sets.xml")
            sets_items = xml.findall('.//{' + utils.xmlns.oai() + '}' + 'set')
            rsets = []
            for s in sets_items:
                setSpec = s.find('.//{' + utils.xmlns.oai() + '}' + 'setSpec')
                setName = s.find('.//{' + utils.xmlns.oai() + '}' + 'setName')
                rsets.append( { setSpec: setName } )
            if not self.repository.data:
                self.repository.data = {}
            self.repository.data['sets'] = rsets


    def get_items(self):
        """retrieve all the identifiers of the source, create a directory structure, and save id.xml for each identified retrieved. Check if the repo object identifier is the same that the directory identifier. If a item directory exist, delete it and continue"""

        xml = self._get_xml_from_file("identify.xml")
        identifier = xml.find('.//{' + utils.xmlns.oai_identifier() + '}repositoryIdentifier')
        if self.repository.identifier is not None and self.repository.identifier != identifier.text:
            # print(self.repository.identifier)
            # print(identifier.text)
            raise IrokoHarvesterError('{0}!={1}. Problems with directory structure. Source.id={3}. '.format(self.repository.identifier, identifier.text, self.source.id))

        if not self.work_remote:
            # TODO: Eliminar todos los harvesterItems y todos los records y pids asociados a este source...
            # db.session.delete?
            for itemdir in listdir(self.harvest_dir):
                itempath = path.join(self.harvest_dir, itemdir)
                if path.isdir(itempath):
                    shutil.move(itempath, path.join(self.harvest_dir, itemdir)+'.old')
            for itemdir in listdir(self.harvest_dir):
                itempath = path.join(self.harvest_dir, itemdir)
                if path.isdir(itempath):
                    idpath = path.join(itempath, "id.xml")
                    if path.exists(idpath):
                        xml = self._get_xml_from_file("id.xml", itemdir)
                        identifier = xml.find('.//{' + utils.xmlns.oai() + '}identifier')
                        harvest_item = HarvestedItem()
                        harvest_item.repository_id = self.source.id
                        harvest_item.identifier = identifier.text
                        harvest_item.status = HarvestedItemStatus.HARVESTED
                        db.session.add(harvest_item)
                        db.session.commit()
                        shutil.move(itempath, path.join(self.harvest_dir, str(harvest_item.id)))
        else:
            iterator = self.sickle.ListIdentifiers(metadataPrefix=self.oai_dc.metadataPrefix)
            count = 0
            for item in iterator:
                harvest_item = HarvestedItem.query.filter_by(repository_id=self.source.id,\
                                    identifier=item.identifier).first()
                try:
                    if harvest_item is None:
                        harvest_item = HarvestedItem()
                        harvest_item.repository_id = self.source.id
                        harvest_item.identifier = item.identifier
                        db.session.add(harvest_item)
                        db.session.commit()
                        p = path.join(self.harvest_dir, str(harvest_item.id))
                        if path.exists(p):
                            raise IrokoHarvesterError('Item.id={0}, already a directoy with that id. harvest_item.identifier={1}. Source.id={2}.'.format(harvest_item.id,harvest_item.identifier, self.source.id))
                        mkdir(p)
                    if item.deleted:
                        harvest_item.status = HarvestedItemStatus.DELETED
                    p = path.join(self.harvest_dir, str(harvest_item.id))

                    if not path.exists(p):
                        mkdir(p)

                    self._write_file("id.xml", item.raw, str(harvest_item.id))

                    if harvest_item.status != HarvestedItemStatus.DELETED:
                        self._get_all_formats(harvest_item)
                        harvest_item.status = HarvestedItemStatus.HARVESTED
                    sleep(self.request_wait_time)
                except Exception as e:
                    harvest_item.status = HarvestedItemStatus.ERROR
                    harvest_item.error_log = traceback.format_exc()
                finally:
                    db.session.commit()
                    count = count + 1
            print("--- {0} harvested".format(count))


    def _get_all_formats(self, item:HarvestedItem):
        """retrieve all the metadata of an item and save it to files"""

        if not self.work_remote:
            return

        for f in self.formats:
            try:
                arguments ={'metadataPrefix':f,'identifier': item.identifier}
                record = self.sickle.GetRecord(**arguments)
                self._write_file(f+".xml", record.raw, str(item.id))
                sleep(self.request_wait_time)
            except Exception as e:
                item.error_log = traceback.format_exc()
        sleep(self.request_wait_time)


    def record_items(self):
        """ process all item, create an IrokoRecord and save/update it"""

        items = HarvestedItem.query.filter_by(repository_id=self.source.id).all()
        for item in items:
            # if item.status == HarvestedItemStatus.HARVESTED:
            try:
                # print('--------------------')
                # print(item.identifier)
                dc = self._process_format(item, self.oai_dc)
                # print(str(self.repository.metadata_formats))
                nlm = None
                if 'nlm' in self.formats:
                    nlm = self._process_format(item, self.nlm)
                    # print(str(nlm))
                data = self._crate_iroko_dict(item, dc, nlm)


                record, status = IrokoRecord.create_or_update(data, dbcommit=True, reindex=True)
                item.status = HarvestedItemStatus.RECORDED
                item.record = record.id
                # print(item.record)
            except Exception as e:
                item.status = HarvestedItemStatus.ERROR
                item.error_log = traceback.format_exc()


    def _process_format(self, item:HarvestedItem, formater: Formater):

        #TODO change xml to .xml esto esta asi por un error en los datos que tengo en la casa...
        xmlpath = path.join(self.harvest_dir, str(item.id), formater.getMetadataPrefix()+".xml")
        if not path.exists(xmlpath):

            # raise IrokoHarvesterError(xmlpath + 'NOT exists!!!. Source:' + self.source.name + " id:" + item.id + " " + item.identifier)
            return None
        # TODO: si llego hasta aqui y es none, habria que intentar harvestear de nuevo...
        # print(xmlpath)
        xml = etree.parse(xmlpath, parser=XMLParser)
        return formater.ProcessItem(xml)


    def _crate_iroko_dict(self, item:HarvestedItem ,dc , nlm=None):

        data = dc
        # print(str(data))
        if nlm is not None:
            data['creators'] = nlm['creators']
            data['contributors'] = nlm['contributors']

        data['source'] = {
            "uuid": str(self.source.uuid),
            "name": str(self.source.name)
            }
        spec_code = data['spec']
        for s in self.source.sets:
            if spec_code == s.setSpec:
                data['spec'] = {
                    "code": str(s.setSpec),
                    "name": str(s.setName)
                    }
        # aqui iria encontrar los tipos de colaboradores usando nlm...
        # tambien es posible hacer un request de los textos completos usando dc.relations
        return data
