
import requests
import os
import shutil

from zipfile import ZipFile

from iroko.harvester.oai.harvester import OaiHarvester
from iroko.harvester.oai.archivist import Archivist
from iroko.harvester.models import Repository, HarvestedItemStatus
import iroko.harvester.utils as  utils
from iroko.sources.models import Source

from flask import current_app
import json

from lxml import etree

from iroko.harvester.html.issn import IssnHarvester
from iroko.harvester.html.miar import MiarHarvester

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)

class PrimarySourceHarvester(object):
    """Top level harvester, use base.Harvester class, for specific sources.
    ahora mismo hace uso solamente del OAIHarvester"""

    @staticmethod
    def include_zip_files_in_dir(zip_dir):
        """trata de crear un Archivist dado cada uno de los zip en un directorio"""
        for item in os.listdir(zip_dir):
            itempath = os.path.join(zip_dir, item)
            if os.path.isfile(itempath):
                arch = Archivist.create_archivist_from_zip(itempath)
                if arch:
                    arch.record_items()


    @staticmethod
    def rescan_and_fix_harvest_dir():
        """rescanea el directorio current_app.config['HARVESTER_DATA_DIRECTORY']
        1- renombra todos los dirs de harvest poniendole el sufijo old
        2- itera por todos los sources y busca si hay alguna carpeta old que le corresponda,
            esto es, mirando en el identify.xml si el baseURL == source.repository.harvest_endpoint
        3- renombra la carpeta old con el source.id corresponiente
        4- TODO: borra todos los items y records asociados al source que se esta reescaneando
        4- relanza el proceso completo de harvest usando work_remote=False
        """
        harvest_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
        for repodir in os.listdir(harvest_dir):
            repopath = os.path.join(harvest_dir, repodir)
            if os.path.isdir(repopath):
                shutil.move(repopath, os.path.join(harvest_dir, repodir)+'.old')
        for repodir in os.listdir(harvest_dir):
            repopath = os.path.join(harvest_dir, repodir)
            if os.path.isdir(repopath):
                print(repopath)
                xmlpath = os.path.join(repopath, "identify.xml")
                if os.path.exists(xmlpath):
                    xml = etree.parse(xmlpath, parser=XMLParser)
                    baseURL = xml.find('.//{' + utils.xmlns.oai + '}baseURL')
                    print(baseURL.text)
                    repository = Repository.query.filter_by(harvest_endpoint=baseURL.text).first()
                    if repository is not None:
                        source = Source.query.filter_by(id=repository.source_id).first()
                        shutil.move(repopath, os.path.join(harvest_dir, str(source.id)))
                        harvester = OaiHarvester(source, False, request_wait_time=0)
                        harvester.repository.status = HarvestedItemStatus.HARVESTED
                        harvester.identity_source()
                        harvester.repository.status = HarvestedItemStatus.HARVESTED
                        harvester.discover_items()
                        harvester.repository.status = HarvestedItemStatus.HARVESTED
                        zip_path = os.path.join(
                            harvest_dir,
                            str(source.uuid) + ".zip"
                        )
                        direct = os.path.join(harvest_dir, str(source.id))
                        with ZipFile(zip_path, 'w') as zipObj:
                            for item in os.listdir(direct):
                                itempath = os.path.join(direct, item)
                                if os.path.isdir(itempath):
                                    for fil in os.listdir(itempath):
                                        filpath = os.path.join(itempath, fil)
                                        zipObj.write(filpath, arcname=os.path.join(item, fil))
                                else:
                                    zipObj.write(itempath, arcname=item)


    @staticmethod
    def rescan_and_fix_source_dir(source_dir):
        """
        3- renombra la carpeta old con el source.id corresponiente
        4- borra todos los items y records asociados al source que se esta reescaneando
        4- relanza el proceso completo de harvest usando work_remote=False
        """
        harvest_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
        repopath = os.path.join(harvest_dir, source_dir)
        if os.path.isdir(repopath):
            shutil.move(repopath, os.path.join(harvest_dir, source_dir)+'.old')
            repopath = os.path.join(harvest_dir, source_dir)+'.old'
            print(repopath)
            xmlpath = os.path.join(repopath, "identify.xml")
            if os.path.exists(xmlpath):
                xml = etree.parse(xmlpath, parser=XMLParser)
                baseURL = xml.find('.//{' + utils.xmlns.oai + '}baseURL')
                print(baseURL.text)
                source = Source.query.filter_by(repo_harvest_endpoint=baseURL.text).first()
                if source is not None:
                    shutil.move(repopath, os.path.join(harvest_dir, str(source.id)))
                    PrimarySourceHarvester.harvest_pipeline(source.id, False)


    @staticmethod
    def process_sources(source_id_list, work_remote=True):
        """ harvest_pipeline por cada source in sources"""
        for source in source_id_list:
            PrimarySourceHarvester.harvest_pipeline(source, work_remote)


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


class SecundarySourceHarvester:
    """top level harvester for the secundary sources, issn, miar, etc...
    this should include sec sources for primary sources (issn, miar,...)
    and secundary sources for harvested items (dimensions, crossref, ...)
    """

    @staticmethod
    def process_issn(remoteissns=True, remoteinfo=True, info=True):

        work_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
        harvester = IssnHarvester(work_dir)

        issns = harvester.get_cuban_issns_json(remoteissns)

        if info:
            infos = harvester.get_cuban_issns_info_json(issns, remoteinfo)
            # con lo que hay en el dic, crear/actualizar, versiones de source cuyo comentario sea issn...

    @staticmethod
    def harvest_miar(recheck=True):
        work_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
        print(work_dir)
        if not recheck:
            harvester = MiarHarvester(work_dir, True)
        else:
            print('recheck is True')
            harvester = MiarHarvester(work_dir, False)
            harvester.get_info_database_recheck()
        # crear el vocabulario miar_databases

    @staticmethod
    def get_cuban_issns():
        work_dir = current_app.config['HARVESTER_DATA_DIRECTORY']
        harvester = IssnHarvester(work_dir)

        issns = harvester.get_cuban_issns_json(False)
        infos = harvester.get_cuban_issns_info_json(issns, False)

        return infos
