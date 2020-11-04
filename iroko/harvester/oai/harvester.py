import os
import shutil
import time
import traceback
import uuid
from enum import Enum
from zipfile import ZipFile, BadZipFile

from flask import current_app
from invenio_db import db
from lxml import etree
from sickle import Sickle

import iroko.harvester.utils as utils
from iroko.harvester.base import SourceHarvester
from iroko.harvester.errors import IrokoHarvesterError
from iroko.harvester.models import HarvestedItem, HarvestedItemStatus, Repository, HarvestType
from iroko.harvester.oai import request_headers
from iroko.harvester.oai.formaters import DubliCoreElements, JournalPublishing
from iroko.sources.api import SourceRecord

# from iroko.sources.models import Source

XMLParser = etree.XMLParser(
    remove_blank_text=True, recover=True, resolve_entities=False
)

class OaiHarvesterFileNames(Enum):
    IDENTIFY = "identify.xml"
    FORMATS = "metadata_formats.xml"
    SETS = "sets.xml"
    ITEM_IDENTIFIER = "id.xml"


class OaiHarvester(SourceHarvester):
    """ esta clase maneja todo lo relacionado con el harvesting de un source, llega hasta insertar/actualizar los HarvesterItems,
    al mismo tiempo, crea una estructura de carpetas donde se almacena todo lo cosechado sin procesar
    dentro de current_app.config['HARVESTER_DATA_DIRECTORY'] crea una carpeta con el UUID del source.
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
    Cuando actualiza la cosecha una fuente, o sea cuando ya se ha cosechado otras veces,
    se modifica la estructura de carpetas si es necesario, si hay que adicionar items, o si cambiaron algunos,etc
    """

    @staticmethod
    def get_source_from_zip(file_path, copy_to_harvest_dir=True):
        """find the corresponding source given a zip file with harvested data
        return None if no source is found or any exception rise with the zip file
        if copy_to_harvest_dir,
            copy the file_path to
            os.path.join(current_app.config["HARVESTER_DATA_DIRECTORY"],
                                str(source.uuid)))
        """
        tmp_dir = os.path.join(
                    current_app.config["IROKO_TEMP_DIRECTORY"],"iroko-harvest-arch-" + str(time.time())
                )
        try:

            with ZipFile(file_path, "r") as zipOpj:

                try:
                    zipOpj.extract(
                    OaiHarvesterFileNames.IDENTIFY.value,
                    tmp_dir
                )
                except Exception:
                    return None

                identify_path = os.path.join(tmp_dir, OaiHarvesterFileNames.IDENTIFY.value)
                xml = utils.get_xml_from_file(
                    current_app.config["IROKO_TEMP_DIRECTORY"],
                    identify_path
                )

                name = xml.find(
                    ".//{" + utils.xmlns.oai + "}repositoryName"
                ).text

                oai_url = xml.find(
                    ".//{" + utils.xmlns.oai + "}baseURL"
                ).text

                identifier = xml.find(
                    ".//{" + utils.xmlns.oai_identifier + "}repositoryIdentifier"
                ).text
                # print("{0}-{1}-{2}".format(name, oai_url, identifier))
                repo = Repository.query.filter_by(harvest_endpoint=oai_url).first()
                if repo:
                    repo.status == None
                    db.session.commit()
                    source = SourceRecord.get_record(repo.source_uuid)
                else:
                    return None
                if(source and copy_to_harvest_dir):
                    source_path = os.path.join(current_app.config["HARVESTER_DATA_DIRECTORY"], str(source.id))
                    if source_path != file_path:
                        if not os.path.exists(source_path):
                            # TODO: if path exists means that a "merge" between the two zip files is needed,
                            #  now assuming that is the same...
                            # 1- compare both files
                            # 2- merge
                            # 3- rescan
                            # if os.path.getsize(file_path) != os.path.getsize(source_path):
                            shutil.rmtree(
                                source_path,
                                True
                            )
                        shutil.move(
                            file_path,
                            source_path
                        )

                shutil.rmtree(
                    tmp_dir,
                    True
                )

                return source

        except (BadZipFile, Exception)  as err:
            # print(err)
            # print(err.args)

            shutil.rmtree(
                    tmp_dir,
                    True
            )
            return None


    @staticmethod
    def rescan_source_from_zip_file(file_path):
        """given zip file, finds the corresponding source and harvest all items using work_remote = false
        """
        source = OaiHarvester.get_source_from_zip(file_path)

        if source:
            harvester = OaiHarvester(source, work_remote=False)
            harvester.start_harvest_pipeline()



    def __init__(self, source: SourceRecord, work_remote=True, request_wait_time=3):

        # init_directory=True
        max_retries = 3

        super().__init__(source, work_remote, request_wait_time)
        # self.source = source
        # self.work_remote = work_remote
        # self.request_wait_time = request_wait_time

        # p = current_app.config["HARVESTER_DATA_DIRECTORY"]
        # p = 'data/sceiba-data'
        source_path = os.path.join(current_app.config["HARVESTER_DATA_DIRECTORY"], str(source.id))
        if not os.path.exists(source_path):
            with ZipFile(source_path, 'w') as file:
                pass

        self.harvest_dir = os.path.join(
            current_app.config["IROKO_TEMP_DIRECTORY"],
            "iroko-harvest-" + str(self.source.id)
        )
        shutil.rmtree(self.harvest_dir, ignore_errors=True)

        with ZipFile(source_path, "r") as zipOpj:
                zipOpj.extractall(self.harvest_dir)

        self.oai_dc = DubliCoreElements()
        self.nlm = JournalPublishing()

        # proxies = {"http": "http://servers-proxy.upr.edu.cu:8080","https": "http://servers-proxy.upr.edu.cu:8080"}
        self.repository = Repository.query.filter_by(source_uuid=self.source.id).first()
        if not self.repository:
            repository = Repository()
            repository.harvest_endpoint = self.source.model.json['oaiurl']
            repository.harvest_type = HarvestType.OAI
            repository.source_uuid = self.source.id
            db.session.add(repository)
            db.session.commit()
        # args = {'headers':request_headers,'proxies':proxies,'timeout':15, 'verify':False}
        args = {"headers": request_headers, "timeout": 15, "verify": False}
        self.sickle = Sickle(
            self.repository.harvest_endpoint,
            encoding='UTF-8',
            max_retries=max_retries,
            **args
        )

    def start_harvest_pipeline(self, step=0):
        """default harvest pipeline, identify, discover, process"""
        if step == 0:
            self.identity_source()
        if step <= 1:
            self.discover_items()
        self.compress_harvest_dir()

    def compress_harvest_dir(self):
        """compress the harvest_dir to a zip file in harvest_data dir
        and deleted harvest_dir """
        shutil.rmtree(
            os.path.join(current_app.config["HARVESTER_DATA_DIRECTORY"], str(self.source.id)),
            ignore_errors=True)
        utils.ZipHelper.compress_dir(self.harvest_dir, current_app.config["HARVESTER_DATA_DIRECTORY"], str(self.source.id))
        shutil.rmtree(self.harvest_dir, ignore_errors=True)

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
            # print("error: identity_source(self):")
            # print(e)
            # print(e.args)
        finally:
            db.session.commit()

    def discover_items(self):
        if self.repository.status == HarvestedItemStatus.ERROR:
            raise IrokoHarvesterError(
                "calling discover_items of in a inestable repo. Source.id={0}. Source.repo_status={1}".format(
                    self.source.id, self.repository.status
                )
            )
        try:
            self.get_items()
            self.repository.status = HarvestedItemStatus.HARVESTED
        except Exception as e:
            self.repository.status = HarvestedItemStatus.ERROR
            self.repository.error_log = traceback.format_exc()
            # print("error: discover_items(self):")
            # print(e)
            # print(e.args)
        finally:
            db.session.commit()

    def _write_file(self, name, content, extra_path=""):
        """helper function, always write to f = open(os.path.join(self.harvest_dir, extra_path, name),"w")"""

        f = open(os.path.join(self.harvest_dir, extra_path, name), "w", encoding='UTF-8')
        f.write(content)
        f.close()

    def _get_xml_from_file(self, name, extra_path=""):
        return utils.get_xml_from_file(self.harvest_dir, name, extra_path=extra_path)
        # xmlpath = os.path.join(self.harvest_dir, extra_path, name)
        # if not os.path.exists(xmlpath):
        #     raise IrokoHarvesterError(
        #         "working offline and {0} not exists. Source.id={1}".format(
        #             xmlpath, self.source.id
        #         )
        #     )
        # return etree.parse(xmlpath, parser=XMLParser)

    def get_identify(self):
        """get_identity, raise IrokoHarvesterError"""
        if self.work_remote:
            identify = self.sickle.Identify()
            xml = identify.xml
            # identifier = identify._identify_dict['repositoryIdentifier']
        else:
            xml = self._get_xml_from_file("identify.xml")
        identifier = xml.find(
            ".//{" + utils.xmlns.oai_identifier + "}repositoryIdentifier"
        ).text

        if (
            self.repository.identifier is not None
            and self.repository.identifier != identifier
        ):
            # identifiers could be different, but this is not an exception
            # for now i will put this error log...
            self.repository.error_log = "Different identifiers: {0}!={1}. Source.id={2}. work_remote:{3}".format(
                self.repository.identifier,
                identifier,
                self.source.id,
                self.work_remote,
            )

        self.repository.identifier = identifier
        if self.work_remote:
            self._write_file("identify.xml", identify.raw)

    def get_formats(self):
        """get_formats, raise IrokoHarvesterError"""

        self.formats = []
        if self.work_remote:
            arguments = {}
            items = self.sickle.ListMetadataFormats(**arguments)
            for f in items:
                self.formats.append(f.metadataPrefix)
            self._write_file("metadata_formats.xml", items.oai_response.raw)
        else:
            xml = self._get_xml_from_file("metadata_formats.xml")
            self.formats = utils.get_multiple_elements(
                xml, "metadataPrefix", xmlns=utils.xmlns.oai
            )
            # print(self.formats)

        self._assing_repository_data_field('formats', self.formats)

        # TODO: a medida que se incluyan los otros formatos, lo que tiene que pasar es que si el repo no soporta ninguno de los formatos del harvester entonces es que se manda la excepcion... pero por el momento si no soporta oai_dc, entonces no se puede cosechar
        if "oai_dc" not in self.formats:
            raise IrokoHarvesterError(
                " oai_dc is not supported by Source.id={0} ".format(self.source.id)
            )

    def get_sets(self):
        """get_sets"""

        sets = []
        if self.work_remote:
            arguments = {}
            items = self.sickle.ListSets(**arguments)
            self._write_file("sets.xml", items.oai_response.raw)
            rsets = []
            for s in items:
                rsets.append({s.setSpec: s.setName})

        else:
            xml = self._get_xml_from_file("sets.xml")
            sets_items = xml.findall(".//{" + utils.xmlns.oai + "}" + "set")
            rsets = []
            for s in sets_items:
                setSpec = s.find(".//{" + utils.xmlns.oai + "}" + "setSpec").text
                setName = s.find(".//{" + utils.xmlns.oai + "}" + "setName").text
                rsets.append({setSpec: setName})

        self._assing_repository_data_field('sets', rsets)

    def _assing_repository_data_field(self, key, value):
        try:
            data = dict(self.repository.data)
        except Exception as ex:
            data = dict()
        data[key] = value
        self.repository.data = data

    def get_items(self):
        """retrieve all the identifiers of the source, create a directory structure, and save id.xml for each identified retrieved. Check if the repo object identifier is the same that the directory identifier. If a item directory exist, delete it and continue"""

        xml = self._get_xml_from_file("identify.xml")
        identifier = xml.find(
            ".//{" + utils.xmlns.oai_identifier + "}repositoryIdentifier"
        )
        if (
            self.repository.identifier is not None
            and self.repository.identifier != identifier.text
        ):
            # # print(self.repository.identifier)
            # # print(identifier.text)
            raise IrokoHarvesterError(
                "{0}!={1}. Problems with directory structure. Source.id={3}. ".format(
                    self.repository.identifier, identifier.text, self.source.id
                )
            )

        if not self.work_remote:
            # TODO: Eliminar todos los harvesterItems y todos los records y pids asociados a este source...
            # db.session.delete?
            for itemdir in os.listdir(self.harvest_dir):
            # for itemdir in os.listdir(fix_path):
                itempath = os.path.join(self.harvest_dir, itemdir)

                if os.path.isdir(itempath):
                    # print(os.path.join(self.harvest_dir, itemdir) + ".old")
                    shutil.move(itempath, os.path.join(self.harvest_dir, itemdir) + ".old")
            for itemdir in os.listdir(self.harvest_dir):
                itempath = os.path.join(self.harvest_dir, itemdir)
                if os.path.isdir(itempath):
                    idpath = os.path.join(itempath, "id.xml")
                    if os.path.exists(idpath):
                        xml = self._get_xml_from_file("id.xml", itemdir)
                        identifier = xml.find(
                            ".//{" + utils.xmlns.oai + "}identifier"
                        )
                        harvest_item = HarvestedItem.query.filter_by(source_uuid = self.source.id, identifier = identifier.text).first()
                        if not harvest_item:
                            # this item hasn't harvested
                            harvest_item = HarvestedItem()
                            harvest_item.source_uuid = self.source.id
                            harvest_item.identifier = identifier.text
                            harvest_item.status = HarvestedItemStatus.HARVESTED
                            db.session.add(harvest_item)
                            db.session.commit()
                        shutil.move(
                            itempath, os.path.join(self.harvest_dir, str(harvest_item.id))
                        )
                        if harvest_item.status == HarvestedItemStatus.ERROR:
                            harvest_item.status = HarvestedItemStatus.HARVESTED

        else:
            iterator = self.sickle.ListIdentifiers(
                metadataPrefix=self.oai_dc.metadataPrefix
            )
            count = 0
            for item in iterator:
                harvest_item = HarvestedItem.query.filter_by(
                    source_uuid=self.source.id, identifier=item.identifier
                ).first()
                try:
                    if harvest_item is None:
                        harvest_item = HarvestedItem()
                        harvest_item.source_uuid = self.source.id
                        harvest_item.identifier = item.identifier
                        db.session.add(harvest_item)
                        db.session.commit()
                        p = os.path.join(self.harvest_dir, str(harvest_item.id))
                        if os.path.exists(p):
                            shutil.move(
                                p, p+ ".old"
                            )
                            # raise IrokoHarvesterError(
                            #     "Item.id={0}, already a directoy with that id. harvest_item.identifier={1}. Source.id={2}.".format(
                            #         harvest_item.id,
                            #         harvest_item.identifier,
                            #         self.source.id,
                            #     )
                            # )
                        os.mkdir(p)
                    if item.deleted:
                        harvest_item.status = HarvestedItemStatus.DELETED
                    p = os.path.join(self.harvest_dir, str(harvest_item.id))

                    if not os.path.exists(p):
                        os.mkdir(p)

                    self._write_file("id.xml", item.raw, str(harvest_item.id))

                    if harvest_item.status != HarvestedItemStatus.DELETED:
                        self._get_all_formats(harvest_item)
                        harvest_item.status = HarvestedItemStatus.HARVESTED
                    time.sleep(self.request_wait_time)
                except Exception as e:
                    harvest_item.status = HarvestedItemStatus.ERROR
                    harvest_item.error_log = traceback.format_exc()
                    # print(e)
                    # print(e.args)
                finally:
                    db.session.commit()
                    count = count + 1
            # print("--- {0} harvested".format(count))

    def _get_all_formats(self, item: HarvestedItem):
        """retrieve all the metadata of an item and save it to files"""

        if not self.work_remote:
            return

        for f in self.formats:
            try:
                arguments = {"metadataPrefix": f, "identifier": item.identifier}
                record = self.sickle.GetRecord(**arguments)
                self._write_file(f + ".xml", record.raw, str(item.id))
                time.sleep(self.request_wait_time)
            except Exception as e:
                item.error_log = traceback.format_exc()
                # print(e)
                # print(e.args)
        time.sleep(self.request_wait_time)


class OaiFetcher:
    """ esta clase maneja todo lo relacionado con el harvesting de un source, llega hasta insertar/actualizar los HarvesterItems,
    al mismo tiempo, crea una estructura de carpetas donde se almacena todo lo cosechado sin procesar
    dentro de current_app.config['HARVESTER_DATA_DIRECTORY'] crea una carpeta con el UUID del source.
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
    Cuando actualiza la cosecha una fuente, o sea cuando ya se ha cosechado otras veces,
    se modifica la estructura de carpetas si es necesario, si hay que adicionar items, o si cambiaron algunos,etc
    """

    def __init__(self, url, request_wait_time=3, data_dir=None):

        max_retries = 3
        timeout = 30

        self.url = url
        self.request_wait_time = request_wait_time
        self.id = str(uuid.uuid4())

        if not data_dir:
            self.data_dir = current_app.config["HARVESTER_DATA_DIRECTORY"]
        else:
            self.data_dir = data_dir

        f = open(os.path.join(self.data_dir, self.id + '-url'), "w", encoding='UTF-8')
        f.write(self.url)
        f.close()

        self.harvest_dir = os.path.join(
            current_app.config["IROKO_TEMP_DIRECTORY"],
            "iroko-harvest-" + str(self.id)
        )
        shutil.rmtree(self.harvest_dir, ignore_errors=True)
        if not os.path.exists(self.harvest_dir):
            os.mkdir(self.harvest_dir)

        self.formats = []
        self.oai_dc = DubliCoreElements()
        self.nlm = JournalPublishing()

        # args = {'headers':request_headers,'proxies':proxies,'timeout':15, 'verify':False}
        args = {"headers": request_headers, "timeout": timeout, "verify": False}
        self.sickle = Sickle(
            self.url,
            encoding='UTF-8',
            max_retries=max_retries,
            **args
        )

    def start_harvest_pipeline(self, step=0):
        """default harvest pipeline, identify, discover, process"""
        try:

            if step == 0:
                self.identity_source()
            if step <= 1:
                self.get_items()
            self.compress_harvest_dir()
            return True
        except Exception as e:
            f = open(os.path.join(self.data_dir, self.id + '-error'), "w", encoding='UTF-8')
            f.write(traceback.format_exc())
            f.close()
            shutil.rmtree(self.harvest_dir, ignore_errors=True)
            return False

    def compress_harvest_dir(self):
        """compress the harvest_dir to a zip file in harvest_data dir
        and deleted harvest_dir """
        shutil.rmtree(
            os.path.join(self.data_dir, str(self.id)),
            ignore_errors=True)
        utils.ZipHelper.compress_dir(self.harvest_dir, self.data_dir, str(self.id))
        shutil.rmtree(self.harvest_dir, ignore_errors=True)

    def identity_source(self):
        self.get_identify()
        self.get_formats()
        self.get_sets()


    def _write_file(self, name, content, extra_path=""):
        """helper function, always write to f = open(os.path.join(self.harvest_dir, extra_path, name),"w")"""

        f = open(os.path.join(self.harvest_dir, extra_path, name), "w", encoding='UTF-8')
        f.write(content)
        f.close()

    def _get_xml_from_file(self, name, extra_path=""):
        return utils.get_xml_from_file(self.harvest_dir, name, extra_path=extra_path)

    def get_identify(self):
        """get_identity, raise IrokoHarvesterError"""
        identify = self.sickle.Identify()
        xml = identify.xml
        self._write_file("identify.xml", identify.raw)

    def get_formats(self):
        """get_formats, raise IrokoHarvesterError"""

        arguments = {}
        items = self.sickle.ListMetadataFormats(**arguments)
        for f in items:
            self.formats.append(f.metadataPrefix)
        self._write_file("metadata_formats.xml", items.oai_response.raw)

        if "oai_dc" not in self.formats:
            self._write_file('error_no_dublin_core', " oai_dc is not supported by {0} ".format(self.url))

    def get_sets(self):
        """get_sets"""
        arguments = {}
        items = self.sickle.ListSets(**arguments)
        self._write_file("sets.xml", items.oai_response.raw)

    def get_items(self):
        """retrieve all the identifiers of the source, create a directory structure,
        and save id.xml for each identified retrieved.
        Check if the repo object identifier is the same that the directory identifier.
        If a item directory exist, delete it and continue"""

        xml = self._get_xml_from_file("identify.xml")
        identifier = xml.find(
            ".//{" + utils.xmlns.oai_identifier + "}repositoryIdentifier"
        )

        iterator = self.sickle.ListIdentifiers(
            metadataPrefix=self.oai_dc.metadataPrefix
        )
        count = 0
        for item in iterator:
            harvest_item_id = str(uuid.uuid4())
            p = os.path.join(self.harvest_dir, harvest_item_id)
            if not os.path.exists(p):
                os.mkdir(p)
            self._write_file("id.xml", item.raw, harvest_item_id)
            self._get_all_formats(item.identifier, harvest_item_id)

            time.sleep(self.request_wait_time)

    def _get_all_formats(self, identifier, harvest_item_id):
        """retrieve all the metadata of an item and save it to files"""

        for f in self.formats:
            try:
                arguments = {"metadataPrefix": f, "identifier": identifier}
                record = self.sickle.GetRecord(**arguments)
                self._write_file(f + ".xml", record.raw, harvest_item_id)
                time.sleep(self.request_wait_time)
            except Exception as e:
                self._write_file('error', traceback.format_exc(), harvest_item_id)
        time.sleep(self.request_wait_time)
