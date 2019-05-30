
import requests
from os import listdir, path
import shutil

from iroko.harvester.oai.harvester import OaiHarvester
from iroko.harvester import utils
from iroko.sources.models import Source

from flask import current_app

from lxml import etree


XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)

class Harvester(object):
    """Top level harvester, use base.Harvester class, for specific sources.
    ahora mismo hace uso solamente del OAIHarvester"""

    @staticmethod
    def rescan_and_fix_harvest_dir():
        """rescanea el directorio current_app.config['HARVESTER_DATA_DIRECTORY']
        1- renombra todos los dirs de harvest poniendole el sufijo old
        2- itera por todos los sources y busca si hay alguna carpeta old que le corresponda,
            esto es, mirando en el identify.xml si el baseURL == source.repo_harvest_endpoint
        3- renombra la carpeta old con el source.id corresponiente
        4- borra todos los items y records asociados al source que se esta reescaneando
        4- relanza el proceso completo de harvest usando work_remote=False
        """
        harvest_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
        for repodir in listdir(harvest_dir):
            repopath = path.join(harvest_dir, repodir)
            if path.isdir(repopath):
                shutil.move(repopath, path.join(harvest_dir, repodir)+'.old')
        for repodir in listdir(harvest_dir):
            repopath = path.join(harvest_dir, repodir)
            if path.isdir(repopath):
                print(repopath)
                xmlpath = path.join(repopath, "identify.xml")
                if path.exists(xmlpath):
                    xml = etree.parse(xmlpath, parser=XMLParser)
                    baseURL = xml.find('.//{' + utils.xmlns.oai() + '}baseURL')
                    print(baseURL.text)
                    source = Source.query.filter_by(repo_harvest_endpoint=baseURL.text).first()
                    if source is not None:
                        shutil.move(repopath, path.join(harvest_dir, str(source.id)))
                        Harvester.harvest_pipeline(source.id, False)
                        
    @staticmethod
    def rescan_and_fix_source_dir(source_dir):
        """
        3- renombra la carpeta old con el source.id corresponiente
        4- borra todos los items y records asociados al source que se esta reescaneando
        4- relanza el proceso completo de harvest usando work_remote=False
        """
        harvest_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
        repopath = path.join(harvest_dir, source_dir)
        if path.isdir(repopath):
            shutil.move(repopath, path.join(harvest_dir, source_dir)+'.old')
            repopath = path.join(harvest_dir, source_dir)+'.old'
            print(repopath)
            xmlpath = path.join(repopath, "identify.xml")
            if path.exists(xmlpath):
                xml = etree.parse(xmlpath, parser=XMLParser)
                baseURL = xml.find('.//{' + utils.xmlns.oai() + '}baseURL')
                print(baseURL.text)
                source = Source.query.filter_by(repo_harvest_endpoint=baseURL.text).first()
                if source is not None:
                    shutil.move(repopath, path.join(harvest_dir, str(source.id)))
                    Harvester.harvest_pipeline(source.id, False)
                        
            

    @staticmethod
    def process_sources(source_id_list, work_remote=True):
        """ harvest_pipeline por cada source in sources"""
        for source in source_id_list:
            Harvester.harvest_pipeline(source, work_remote)

    @staticmethod
    def harvest_pipeline(source_id: int, work_remote=True, step=0):
        """default harvest pipeline, identify, discover, process"""
        source = Source.query.filter_by(id=source_id).first()
        if source is not None:
            harvester = OaiHarvester(source, work_remote=work_remote, request_wait_time=0)
            if step == 0:
                harvester.identity_source()
            if step <= 1:
                harvester.discover_items()
            if step <= 2:
                harvester.process_items()
