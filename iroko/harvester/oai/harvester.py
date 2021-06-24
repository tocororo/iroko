#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import os
import shutil
import time
import traceback
import uuid
from enum import Enum
from zipfile import BadZipFile, ZipFile

from flask import current_app
from invenio_db import db
from lxml import etree
from sickle import Sickle

import iroko.harvester.utils as utils
from iroko.harvester.base import Formater
from iroko.harvester.errors import IrokoHarvesterError
from iroko.harvester.models import HarvestType, HarvestedItem, HarvestedItemStatus, Repository
from iroko.harvester.oai import request_headers
from iroko.harvester.oai.formaters import DubliCoreElements, JournalPublishing
from iroko.records.api import IrokoRecord
from iroko.sources.api import SourceRecord
# from iroko.sources.models import Source
from iroko.utils import IrokoVocabularyIdentifiers
from iroko.vocabularies.models import Term, Vocabulary

XMLParser = etree.XMLParser(
    remove_blank_text=True, recover=True, resolve_entities=False
    )


def get_current_data_dir():
    return current_app.config["HARVESTER_DATA_DIRECTORY"]


def get_source_from_zip(zip_file_path):
    """
    find the corresponding SourceRecord given a zip file with harvested data
    return None if no source is found or any exception rise with the zip file
    :param zip_file_path:
    :return:
    """

    tmp_dir = os.path.join(
        current_app.config["IROKO_TEMP_DIRECTORY"], "iroko-harvest-arch-" + str(time.time())
        )
    try:
        with ZipFile(zip_file_path, "r") as zipOpj:

            try:
                zipOpj.extract(
                    OaiHarvesterFileNames.IDENTIFY.value,
                    tmp_dir
                    )
            except Exception:
                return None

            xml = utils.get_xml_from_file(
                tmp_dir,
                OaiHarvesterFileNames.IDENTIFY.value
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
            pid, source = SourceRecord.get_source_by_pid(oai_url)
            if not pid or not source:
                return None

            shutil.rmtree(
                tmp_dir,
                True
                )

            return source

    except (BadZipFile, Exception) as err:
        # print(err)
        # print(err.args)

        shutil.rmtree(
            tmp_dir,
            True
            )
        return None


class OaiHarvesterFileNames(Enum):
    IDENTIFY = "identify.xml"
    FORMATS = "metadata_formats.xml"
    SETS = "sets.xml"
    ITEM_IDENTIFIER = "id.xml"


class OaiHarvester:

    @staticmethod
    def process_repo(repo: Repository):
        """
        overall process
        :param repo:
        :return:
        """
        file_path = OaiFetcher.fetch_url(repo.harvest_endpoint)
        source_id = OaiFetcherProcessor.process_file(file_path)
        OaiArchivist.archive_source(source_id)

    @staticmethod
    def scan_file(file_path, dst_dir=None):
        """
        procesa un zip y lo guarda en dst_dir
        :param file_path: zip path
        :param dst_dir: directorio destino
        :return:
        """
        if not dst_dir:
            dst_dir = get_current_data_dir()

        if os.path.isfile(file_path):
            try:
                source_id = OaiFetcherProcessor.process_file(file_path, dst_dir)
                OaiArchivist.archive_source(source_id, dst_dir)
            except Exception as e:
                print(e)

    @staticmethod
    def scan_dir(src_dir=None, dst_dir=None):
        """
        procesa todos los zip en el directorio src_dir y los guarda en dst_dir
        :param src_dir: directorio fuente
        :param dst_dir: directorio destino
        :return:
        """
        if not dst_dir:
            dst_dir = get_current_data_dir()
        if not src_dir:
            src_dir = get_current_data_dir()

        for item in os.listdir(src_dir):
            item_path = os.path.join(src_dir, item)
            if os.path.isfile(item_path):
                try:
                    source_id = OaiFetcherProcessor.process_file(item_path, dst_dir)
                    OaiArchivist.archive_source(source_id, dst_dir)
                except Exception as e:
                    print(e)

    @staticmethod
    def fetch_all_repos(data_dir=None):
        repos = Repository.query.all()
        for repo in repos:
            OaiFetcher.fetch_url(repo.harvest_endpoint, data_dir=data_dir)


class OaiArchivist:
    """
    Recibe un source
    - busca en el data dir el zip asociado
    - lo expande en tmp dir

    - se encarga de trabajar con los HarvestedItems:
        - tomar lo que hay en los ficheros
        -
    """

    @classmethod
    def archive_source(cls, source_id, data_dir=None):
        archivist = OaiArchivist(source_id, data_dir)
        archivist.record_items()
        archivist.destroy_work_dir()

    def __init__(self, source_id, data_dir=None):

        if not data_dir:
            self.data_dir = get_current_data_dir()
        else:
            self.data_dir = data_dir

        self.oai_dc = DubliCoreElements()
        self.nlm = JournalPublishing()

        self.source = SourceRecord.get_record(source_id)
        if not self.source:
            raise Exception(
                "You passed the ID={0}, but is not valid. "
                "You cannot instantiate an Archivist without a valid Source".format(
                    source_id
                    )
                )

        self.repository = Repository.query.filter_by(source_uuid=self.source.id).first()
        if not self.repository:
            raise Exception(
                "Source {0}-{1}, has not a associated Repository. "
                "You cannot instantiate an Archivist without an "
                "associated Repository".format(
                    self.source.id, self.source.model.json['title']
                    )
                )

        self.working_dir = os.path.join(
            current_app.config["IROKO_TEMP_DIRECTORY"],
            "iroko-harvest-" + str(self.source.id)
            )
        shutil.rmtree(self.working_dir, ignore_errors=True)

        zip_path = os.path.join(self.data_dir, str(self.source.id))
        try:
            with ZipFile(zip_path, "r") as zipOpj:
                zipOpj.extractall(self.working_dir)
        except Exception as exc:
            raise Exception(
                "ZipFile.extractall({0}) rise an Exception."
                "Source {1}-{2}. You cannot instantiate an Archivist without unzip {0}. "
                "ZipFile Exception:  ####### {3} #######".format(
                    zip_path, self.source.id, self.source.model.json['title'],
                    traceback.format_exc()
                    )
                )

        if not self._check_source_harvested_identification():
            raise Exception(
                "Source {0}-{1}. "
                "Repository harvest_endpoint or identifier is not equal to the values in the zip "
                "file. "
                "Dig into this to instantiate the Archivist".format(
                    self.source.id, self.source.model.json['title']
                    )
                )

        self._fix_repository_data_field()
        self._update_record_set_vocabulary()

    def _check_source_harvested_identification(self):
        """
        check if harvested identifiers are equal to what is in the database
        """

        xml = utils.get_xml_from_file(
            self.working_dir, OaiHarvesterFileNames.IDENTIFY.value
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

        # TODO names should be equals, fix this in source? a new source Version?
        # name == self.source.name and

        return oai_url == self.repository.harvest_endpoint and identifier == \
               self.repository.identifier

    def _fix_repository_data_field(self):
        """
        replace the repository.data field with formats and sets of the OAI protocol
        """

        # source_data = dict(self.source.model)
        try:
            # TODO: currently (11-feb-2020), harvester is creating bad data in the form:
            # "['marcxml', 'rfc1807', 'oai_marc', 'oai_dc', 'nlm']", meaning an array, not dict
            # so, if data is already good, ok
            repo_data = dict(self.repository.data)
        except Exception as ex:
            # if data is not ok, then create a new dict and the method will fixit.
            repo_data = dict()

        xml = utils.get_xml_from_file(self.working_dir, OaiHarvesterFileNames.FORMATS.value)
        self.formats = utils.get_multiple_elements(
            xml, "metadataPrefix", xmlns=utils.xmlns.oai
            )
        repo_data['formats'] = self.formats

        xml = utils.get_xml_from_file(self.working_dir, OaiHarvesterFileNames.SETS.value)

        sets_items = xml.findall(".//{" + utils.xmlns.oai + "}" + "set")
        rsets = []
        for s in sets_items:
            setSpec = s.find(".//{" + utils.xmlns.oai + "}" + "setSpec").text
            setName = s.find(".//{" + utils.xmlns.oai + "}" + "setName").text
            rsets.append({setSpec: setName})
        repo_data['sets'] = rsets

        xml = utils.get_xml_from_file(
            self.working_dir, OaiHarvesterFileNames.IDENTIFY.value
            )
        email = xml.find(
            ".//{" + utils.xmlns.oai + "}adminEmail"
            ).text
        repo_data['email'] = email

        self.repository.data = repo_data

        # TODO: do and SourceRecord update
        # if not 'email' in source_data:
        #     source_data['email'] = email
        #     self.source.data = source_data

        db.session.commit()

    def _update_record_set_vocabulary(self):
        """
        use the sets in the oai repo to create terms in the recod_sets vocabulary
        term in this vocabulary later can be merge manually in order to get another
        classification of articles
        """
        self.voc = Vocabulary.query.filter_by(
            identifier=IrokoVocabularyIdentifiers.RECOD_SETS.value
            ).first()

        xml = utils.get_xml_from_file(self.working_dir, OaiHarvesterFileNames.SETS.value)

        sets_items = xml.findall(".//{" + utils.xmlns.oai + "}" + "set")
        rsets = []
        for s in sets_items:
            setName = s.find(".//{" + utils.xmlns.oai + "}" + "setName").text
            term = Term.query.filter_by(
                vocabulary_id=self.voc.identifier, identifier=setName
                ).first()
            if not term:
                term = Term()
                term.identifier = setName
                term.vocabulary_id = self.voc.identifier
                db.session.add(term)
        db.session.commit()

    #  TODO: esta clase supone que la carpeta esta correctamente formada.
    # lo que sigue debe ser funcion de la clase harvester, que es la que garantiza formar bien la
    # carpeta.
    # if not item:
    # then create a valid HarvestedItem and fix the directory
    # item = HarvestedItem()
    # item.repository_id = self.source.id
    # item.identifier = identifier
    # # TODO: check if item status is deleted.
    # item.status = HarvestedItemStatus.HARVESTED
    # db.session.add(item)
    # db.session.commit()
    # shutil.move(
    #     itempath, os.path.join(self.working_dir, str(item.id))
    # )

    def record_items(self):
        """ process all harvested items of the Source, create an IrokoRecord and save/update it"""

        items = HarvestedItem.query.filter_by(source_uuid=self.source.id).all()
        for item in items:
            try:
                # currently supporting dc elements and nlm (to get more info about authors)
                if item.status != HarvestedItemStatus.DELETED:
                    # and item.status != HarvestedItemStatus.ERROR:

                    dc = self._process_format(item, self.oai_dc)
                    if dc is not None:
                        nlm = None
                        if "nlm" in self.formats:
                            nlm = self._process_format(item, self.nlm)

                        data = self._crate_iroko_dict(item, dc, nlm)
                        # # print(data)

                        record, status = IrokoRecord.create_or_update(
                            data, dbcommit=True, reindex=True
                            )
                        item.status = HarvestedItemStatus.RECORDED
                        item.record = record.id
                        # print(item.record)
                    else:
                        print(
                            "dublin core is none, nothing to do: item: {0}".format(item.identifier)
                            )
                        pass
            except Exception as e:
                item.status = HarvestedItemStatus.ERROR
                item.error_log = traceback.format_exc()
            finally:
                db.session.commit()

    def destroy_work_dir(self):
        """this should be called after record_items, or in any other moment.
        The object do not handle delete work_dir"""

        shutil.rmtree(self.working_dir, ignore_errors=True)

    def _process_format(self, item: HarvestedItem, formater: Formater):

        try:
            xml = utils.get_xml_from_file(
                self.working_dir, formater.getMetadataPrefix() + ".xml",
                extra_path=str(item.id)
                )
            return formater.ProcessItem(xml)
        except Exception as e:
            # nothing to do...
            # TODO: if this is none try to collect this format again
            # (only one time, until the next global iteration over the source)
            return None

    def _crate_iroko_dict(self, item: HarvestedItem, dc, nlm=None):

        data = dict(dc)
        # # print(str(data))
        if nlm is not None:
            data["creators"] = nlm["creators"]
            data["contributors"] = nlm["contributors"]

        data["source_repo"] = {
            "uuid": str(self.source.id), "name": str(self.source.model.json['title'])
            }
        spec_code = data["spec"]
        for s in self.repository.data['sets']:
            for k, v in s.items():
                if spec_code == k:
                    data["spec"] = {"code": k, "name": v}
        # aqui iria encontrar los tipos de colaboradores usando nlm...
        # tambien es posible hacer un request de los textos completos usando dc.relations

        self._update_item_data_vocabularies(data)

        data['status'] = self.source.model.json['source_status']
        return data

    def _update_item_data_vocabularies(self, data):
        """update a record data based on the source relations with specific vocabularies:
        institutions
        grupo_mes
        miar_types
        miar_databases
        unesco_vocab
        """

        # ts = TermSources.query.filter_by(source_id=self.source.id).all()

        data['organizations'] = self.source.model.json['organizations']
        data['classifications'] = self.source.model.json['classifications']

        #
        # tuus = []
        # for ts in self.source.term_sources:
        #     tuus.append(str(ts.term.uuid))
        #
        # rs_term = Term.query.filter_by(vocabulary_id=self.voc.identifier, name=data['spec'][
        # 'name']).first()
        # if rs_term:
        #     tuus.append(str(rs_term.uuid))
        # data['terms'] = tuus

    def _udate_record_type(self, data):
        """ update or define a record_type, based on record_set
        record_set should have a record_type as a class
        if the record_set in the data has a record_type associated,
        then the corresponding record_type will be associated into the data.
        """
        pass


class OaiFetcherProcessor:
    """
    recibe un zip, resultado de OaiFetcher.start_harvest_pipeline()

    """

    @classmethod
    def process_file(cls, file_path, data_dir=None):
        """
        process a zip file
        :param file_path:
        :param data_dir:
        :return: the source.id
        """
        processor = OaiFetcherProcessor(file_path, data_dir)
        return processor.start_process_pipeline()

    def __init__(self, zip_file_path, data_dir=None):

        if not data_dir:
            self.data_dir = get_current_data_dir()
        else:
            self.data_dir = data_dir

        self.source = get_source_from_zip(zip_file_path)
        if not self.source:
            raise Exception('{0}, not contains a valid SourceRecord'.format(zip_file_path))

        self.repository = Repository.query.filter_by(source_uuid=self.source.id).first()
        if not self.repository:
            repository = Repository()
            repository.harvest_endpoint = self.source.model.json['oaiurl']
            repository.harvest_type = HarvestType.OAI
            repository.source_uuid = self.source.id
            db.session.add(repository)
            db.session.commit()

        source_path = os.path.join(self.data_dir, str(self.source.id))
        if os.path.exists(source_path):
            shutil.rmtree(source_path)
        shutil.move(
            zip_file_path,
            source_path
            )

        self.harvest_dir = os.path.join(
            current_app.config["IROKO_TEMP_DIRECTORY"],
            "iroko-harvest-" + str(self.source.id)
            )
        shutil.rmtree(self.harvest_dir, ignore_errors=True)

        with ZipFile(source_path, "r") as zipOpj:
            zipOpj.extractall(self.harvest_dir)

        self.formats = []

    def start_process_pipeline(self):
        """default harvest pipeline, identify, discover, process"""
        try:
            self.identity_source()
            self.discover_items()
            self.compress_harvest_dir()
            return self.source.id
        except Exception as e:
            shutil.rmtree(self.harvest_dir, ignore_errors=True)
            print(traceback.format_exc())

    def compress_harvest_dir(self):
        """compress the harvest_dir to a zip file in harvest_data dir
        and deleted harvest_dir """
        shutil.rmtree(
            os.path.join(self.data_dir, str(self.source.id)),
            ignore_errors=True
            )
        utils.ZipHelper.compress_dir(self.harvest_dir, self.data_dir, str(self.source.id))
        shutil.rmtree(self.harvest_dir, ignore_errors=True)

    def identity_source(self):
        try:
            self.get_identify()
            self.get_formats()
            self.get_sets()
            self.repository.status = HarvestedItemStatus.IDENTIFIED
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
                "calling discover_items of in a inestable repo. Source.id={0}. "
                "Source.repo_status={1}".format(
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

    def _get_xml_from_file(self, name, extra_path=""):
        return utils.get_xml_from_file(self.harvest_dir, name, extra_path=extra_path)

    def get_identify(self):
        """get_identity, raise IrokoHarvesterError"""
        xml = self._get_xml_from_file(OaiHarvesterFileNames.IDENTIFY.value)
        identifier = xml.find(
            ".//{" + utils.xmlns.oai_identifier + "}repositoryIdentifier"
            ).text

        if (
            self.repository.identifier is not None
            and self.repository.identifier != identifier
        ):
            # identifiers could be different, but this is not an exception
            # for now i will put this error log...
            self.repository.error_log = "Different identifiers: {0}!={1}. Source.id={2}.".format(
                self.repository.identifier,
                identifier,
                self.source.id,
                )

        self.repository.identifier = identifier

    def get_formats(self):
        """get_formats, raise IrokoHarvesterError"""

        xml = self._get_xml_from_file(OaiHarvesterFileNames.FORMATS.value)
        self.formats = utils.get_multiple_elements(
            xml, "metadataPrefix", xmlns=utils.xmlns.oai
            )
        self._add_repository_data_field('formats', self.formats)

        # TODO: a medida que se incluyan los otros formatos,
        #  lo que tiene que pasar es que si el repo no soporta ninguno de los formatos del harvester
        #  entonces es que se manda la excepcion...
        #  pero por el momento si no soporta oai_dc, entonces no hay nada que hacer
        if "oai_dc" not in self.formats:
            raise IrokoHarvesterError(
                " oai_dc is not supported by Source.id={0} ".format(self.source.id)
                )

    def get_sets(self):
        """get_sets"""

        xml = self._get_xml_from_file(OaiHarvesterFileNames.SETS.value)
        sets_items = xml.findall(".//{" + utils.xmlns.oai + "}" + "set")
        rsets = []
        for s in sets_items:
            setSpec = s.find(".//{" + utils.xmlns.oai + "}" + "setSpec").text
            setName = s.find(".//{" + utils.xmlns.oai + "}" + "setName").text
            rsets.append({setSpec: setName})

        self._add_repository_data_field('sets', rsets)

    def _add_repository_data_field(self, key, value):
        try:
            data = dict(self.repository.data)
        except Exception as ex:
            data = dict()
        data[key] = value
        self.repository.data = data

    def get_items(self):
        """retrieve all the identifiers of the source, create a directory structure, and save
        id.xml for each identified retrieved. Check if the repo object identifier is the same
        that the directory identifier. If a item directory exist, delete it and continue"""

        xml = self._get_xml_from_file(OaiHarvesterFileNames.IDENTIFY.value)
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
        # TODO: Eliminar todos los harvesterItems y todos los records y pids asociados a este
        #  source...
        # db.session.delete?
        for itemdir in os.listdir(self.harvest_dir):
            itempath = os.path.join(self.harvest_dir, itemdir)
            if os.path.isdir(itempath):
                shutil.move(itempath, os.path.join(self.harvest_dir, itemdir) + ".old")
        for itemdir in os.listdir(self.harvest_dir):
            itempath = os.path.join(self.harvest_dir, itemdir)
            if os.path.isdir(itempath):
                idpath = os.path.join(itempath, OaiHarvesterFileNames.ITEM_IDENTIFIER.value)
                if os.path.exists(idpath):
                    xml = self._get_xml_from_file(
                        OaiHarvesterFileNames.ITEM_IDENTIFIER.value, itemdir
                        )
                    identifier = xml.find(
                        ".//{" + utils.xmlns.oai + "}identifier"
                        )
                    harvest_item = HarvestedItem.query.filter_by(
                        source_uuid=self.source.id,
                        identifier=identifier.text
                        ).first()
                    if not harvest_item:
                        # this item hasn't harvested
                        harvest_item = HarvestedItem()
                        harvest_item.source_uuid = self.source.id
                        harvest_item.identifier = identifier.text
                        harvest_item.status = HarvestedItemStatus.IDENTIFIED
                        db.session.add(harvest_item)
                        db.session.commit()
                    shutil.move(
                        itempath, os.path.join(self.harvest_dir, str(harvest_item.id))
                        )
                    if harvest_item.status == HarvestedItemStatus.ERROR:
                        harvest_item.status = HarvestedItemStatus.IDENTIFIED


class OaiFetcher:
    """ esta clase se encarga de recolectar un OAI endpoint.
    crea una estructura de carpetas donde se almacena todo lo cosechado sin procesar
    dentro de data_dir guarda un zip con un UUID como nombre que dentro tiene:
        1- ficheros con el response de los siguientes verbos:
            - identify.xml
            - metadata_formats.xml
            - sets.xml
        2- carpetas con uuid aleatorios como nombre por cada record, con la forma:
            - id.xml
            - metadata_format_1.xml
            - metadata_format_2.xml
            - fulltext_1.ext
            - fulltext_2.ext
    """

    @classmethod
    def fetch_url(cls, url, data_dir=None, wait_time=3):
        fetcher = OaiFetcher(url, data_dir=data_dir, request_wait_time=wait_time)
        return fetcher.start_harvest_pipeline()

    def __init__(self, url, data_dir=None, request_wait_time=3):

        max_retries = 3
        timeout = 30

        self.url = url
        self.request_wait_time = request_wait_time
        self.id = str(uuid.uuid4())

        if not data_dir:
            self.data_dir = get_current_data_dir()
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

    def start_harvest_pipeline(self):
        """default harvest pipeline, identify, discover, process"""
        try:
            self.identity_source()
            self.get_items()
            return self.compress_harvest_dir()
        except Exception as e:
            f = open(os.path.join(self.data_dir, self.id + '-error'), "w", encoding='UTF-8')
            f.write(traceback.format_exc())
            f.close()
            shutil.rmtree(self.harvest_dir, ignore_errors=True)
            return None

    def compress_harvest_dir(self):
        """compress the harvest_dir to a zip file in harvest_data dir
        and deleted harvest_dir """
        shutil.rmtree(
            os.path.join(self.data_dir, str(self.id)),
            ignore_errors=True
            )
        utils.ZipHelper.compress_dir(self.harvest_dir, self.data_dir, str(self.id))
        shutil.rmtree(self.harvest_dir, ignore_errors=True)
        return os.path.join(self.data_dir, str(self.id))

    def identity_source(self):
        self.get_identify()
        self.get_formats()
        self.get_sets()

    def _write_file(self, name, content, extra_path=""):
        """helper function, always write to f = open(os.path.join(self.harvest_dir, extra_path,
        name),"w")"""

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
            self._write_file(
                'error_no_dublin_core', " oai_dc is not supported by {0} ".format(self.url)
                )

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


class OaiHarvesterDeprecated:
    """ esta clase maneja todo lo relacionado con el harvesting de un source, llega hasta
    insertar/actualizar los HarvesterItems,
    al mismo tiempo, crea una estructura de carpetas donde se almacena todo lo cosechado sin
    procesar
    dentro de current_app.config['HARVESTER_DATA_DIRECTORY'] crea una carpeta con el UUID del
    source.
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
    Cuando se cosecha una fuente por primera vez se crea la estructura de carpetas y se almacena
    en la base de datos lo necesario.
    Cuando actualiza la cosecha una fuente, o sea cuando ya se ha cosechado otras veces,
    se modifica la estructura de carpetas si es necesario, si hay que adicionar items,
    o si cambiaron algunos,etc
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
            current_app.config["IROKO_TEMP_DIRECTORY"], "iroko-harvest-arch-" + str(time.time())
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
                if (source and copy_to_harvest_dir):
                    source_path = os.path.join(get_current_data_dir(), str(source.id))
                    if source_path != file_path:
                        if not os.path.exists(source_path):
                            # TODO: if path exists means that a "merge" between the two zip files
                            #  is needed,
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
        """given zip file, finds the corresponding source and harvest all items using work_remote
        = false
        """
        source = get_source_from_zip(file_path)

        if source:
            harvester = OaiHarvesterDeprecated(source, work_remote=False)
            harvester.start_harvest_pipeline()

    def __init__(self, source: SourceRecord, work_remote=True, request_wait_time=3):

        # init_directory=True
        max_retries = 3

        super().__init__(source, work_remote, request_wait_time)
        # self.source = source
        # self.work_remote = work_remote
        # self.request_wait_time = request_wait_time

        # p = get_current_data_dir()
        # p = 'data/sceiba-data'
        source_path = os.path.join(get_current_data_dir(), str(source.id))
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

        # proxies = {"http": "http://servers-proxy.upr.edu.cu:8080","https":
        # "http://servers-proxy.upr.edu.cu:8080"}
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
            os.path.join(get_current_data_dir(), str(self.source.id)),
            ignore_errors=True
            )
        utils.ZipHelper.compress_dir(
            self.harvest_dir, get_current_data_dir(),
            str(self.source.id)
            )
        shutil.rmtree(self.harvest_dir, ignore_errors=True)

    def identity_source(self):
        try:
            self.get_identify()
            self.get_formats()
            self.get_sets()
            # TODO: habria que analizar denuevo esto.. falta un status que seria identified.. o
            #  ver si esto funciona asi..
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
                "calling discover_items of in a inestable repo. Source.id={0}. "
                "Source.repo_status={1}".format(
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
        """helper function, always write to f = open(os.path.join(self.harvest_dir, extra_path,
        name),"w")"""

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
            self.repository.error_log = "Different identifiers: {0}!={1}. Source.id={2}. " \
                                        "work_remote:{3}".format(
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

        self._add_repository_data_field('formats', self.formats)

        # TODO: a medida que se incluyan los otros formatos, lo que tiene que pasar es que si el
        #  repo no soporta ninguno de los formatos del harvester entonces es que se manda la
        #  excepcion... pero por el momento si no soporta oai_dc, entonces no se puede cosechar
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

        self._add_repository_data_field('sets', rsets)

    def _add_repository_data_field(self, key, value):
        try:
            data = dict(self.repository.data)
        except Exception as ex:
            data = dict()
        data[key] = value
        self.repository.data = data

    def get_items(self):
        """retrieve all the identifiers of the source, create a directory structure, and save
        id.xml for each identified retrieved. Check if the repo object identifier is the same
        that the directory identifier. If a item directory exist, delete it and continue"""

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
            # TODO: Eliminar todos los harvesterItems y todos los records y pids asociados a este
            #  source...
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
                        harvest_item = HarvestedItem.query.filter_by(
                            source_uuid=self.source.id,
                            identifier=identifier.text
                            ).first()
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
                                p, p + ".old"
                                )
                            # raise IrokoHarvesterError(
                            #     "Item.id={0}, already a directoy with that id.
                            #     harvest_item.identifier={1}. Source.id={2}.".format(
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

# Traceback (most recent call last):  File "/Users/malayo/Documents/dev/tocororo/iroko/iroko/iroko/harvester/oai/harvester.py",
# line 376, in record_items    data, dbcommit=True, reindex=True  File "/Users/malayo/Documents/dev/tocororo/iroko/iroko/iroko/records/api.py",
# line 89, in create_or_update    record = cls.get_record_by_data(data)  File "/Users/malayo/Documents/dev/tocororo/iroko/iroko/iroko/records/api.py", line 156, in get_record_by_data
# pid = cls.oai_provider.get_pid_from_data(data=data)  File "/Users/malayo/Documents/dev/tocororo/iroko/iroko/iroko/pidstore/providers.py",
# line 76, in get_pid_from_data    assert 'source' in data, "no source in data"AssertionError: no source in data
