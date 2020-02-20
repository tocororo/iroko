import os

from zipfile import ZipFile

import time

import traceback

import shutil

from lxml import etree

from sickle import Sickle

from flask import current_app

from invenio_db import db

from iroko.sources.models import Source, TermSources, SourceStatus

from iroko.harvester.models import HarvestedItem, HarvestedItemStatus, Repository

from iroko.harvester.oai import nsmap, request_headers
from iroko.harvester.oai.formaters import DubliCoreElements, JournalPublishing
from iroko.harvester.errors import IrokoHarvesterError
import iroko.harvester.utils as utils

import iroko.harvester.oai.harvester as harvester

from iroko.taxonomy.models import Term, Vocabulary

from iroko.harvester.base import SourceHarvester, Formater

from iroko.records.api import IrokoRecord

# PAra que la consola haga autoreaload
# In [1]: %load_ext autoreload

# In [2]: %autoreload 2


class Archivist:
    """
    Recibe un source
    - busca en el data dir el zip asociado
    - lo expande en tmp dir

    - se encarga de trabajar con los HarvestedItems:
        - tomar lo que hay en los ficheros
        -
    """

    @staticmethod
    def create_archivist_from_zip(file_path):
        """find the corresponding source given a zip file with harvested data
        and return an Archivist, return None if no source is found or any exception rise with the zip file
        before create and return the archivist, rename the given zip to HARVESTER_DATA_DIRECTORY using the uuid of the  source
        """

        try:
            source = harvester.OaiHarvester.get_source_from_zip(file_path)
            if (source):
                return Archivist(source.id)
            else:
                return None
        except Exception:
            print(traceback.format_exc())
            return None

    @staticmethod
    def record_items_from_zip(file_path):
        arch = Archivist.create_archivist_from_zip(file_path)
        if arch:
            arch.record_items()
            arch.destroy_work_dir()

    def __init__(self, source_id):

        self.source = Source.query.filter_by(id=source_id).first()
        if not self.source:
            raise Exception(
                "You passed the ID={0}, but is not valid. You cannot instantiate an Archivist without a valid Source".format(
                    source_id
                )
            )

        self.repository = Repository.query.filter_by(source_id=self.source.id).first()
        if not self.repository:
            raise Exception(
                "Source {0}-{1}, has not a associated Repository. You cannot instantiate an Archivist without an associated Repository".format(
                    self.source.id, self.source.name
                )
            )

        self.working_dir = os.path.join(
            current_app.config["IROKO_TEMP_DIRECTORY"],
            "iroko-harvest-" + str(self.source.uuid)
        )
        shutil.rmtree(self.working_dir, ignore_errors=True)

        zip_path = os.path.join(
            current_app.config["HARVESTER_DATA_DIRECTORY"] ,str(self.source.uuid)
        )
        try:
            with ZipFile(zip_path, "r") as zipOpj:
                zipOpj.extractall(self.working_dir)
        except Exception as exc:
            raise Exception(
                "ZipFile.extractall({0}) rise an Exception. Source {1}-{2}. You cannot instantiate an Archivist without unzip {0}. ZipFile Exception:  ####### {3} #######".format(
                    zip_path, self.source.id, self.source.name, traceback.format_exc()
                )
            )

        if not self._check_source_harvested_identification():
            raise Exception(
                "Source {0}-{1}. Repository harvest_endpoint or identifier is not equal to the values in the zip file. Digg into this to instantiate the Archivist".format(
                    self.source.id, self.source.name
                )
            )

        self._fix_repository_data_field()
        self._update_record_set_vocabulary()


    def _check_source_harvested_identification(self):
        """
        check if harvested identifiers are equal to what is in the database
        """

        xml = utils.get_xml_from_file(
            self.working_dir, harvester.OaiHarvesterFileNames.IDENTIFY.value
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

        return oai_url == self.repository.harvest_endpoint and identifier == self.repository.identifier


    def _fix_repository_data_field(self):
        """
        replace the repository.data field with formats and sets of the OAI protocol
        """

        source_data = dict(self.source.data)
        try:
            # TODO: currently (11-feb-2020), harvester is creating bad data in the form:
            # "['marcxml', 'rfc1807', 'oai_marc', 'oai_dc', 'nlm']", meaning an array, not dict
            # so, if data is already good, ok
            repo_data = dict(self.repository.data)
        except Exception as ex:
            # if data is not ok, then create a new dict and the method will fixit.
            repo_data = dict()

        xml = utils.get_xml_from_file(self.working_dir, harvester.OaiHarvesterFileNames.FORMATS.value)
        self.formats = utils.get_multiple_elements(
                xml, "metadataPrefix", xmlns=utils.xmlns.oai
            )
        repo_data['formats'] = self.formats

        xml = utils.get_xml_from_file(self.working_dir, harvester.OaiHarvesterFileNames.SETS.value)

        sets_items = xml.findall(".//{" + utils.xmlns.oai + "}" + "set")
        rsets = []
        for s in sets_items:
            setSpec = s.find(".//{" + utils.xmlns.oai + "}" + "setSpec").text
            setName = s.find(".//{" + utils.xmlns.oai + "}" + "setName").text
            rsets.append({setSpec: setName})
        repo_data['sets'] = rsets

        xml = utils.get_xml_from_file(
            self.working_dir, harvester.OaiHarvesterFileNames.IDENTIFY.value
        )
        email = xml.find(
            ".//{" + utils.xmlns.oai + "}adminEmail"
        ).text
        repo_data['email'] = email

        self.repository.data = repo_data

        if not 'email' in source_data:
            source_data['email'] = email
            self.source.data = source_data

        db.session.commit()


    def _update_record_set_vocabulary(self):
        """
        use the sets in the oai repo to create terms in the recod_sets vocabulary
        term in this vocabulary later can be merge manually in order to get another classification of articles
        """
        self.voc = Vocabulary.query.filter_by(name='record_sets').first()

        xml = utils.get_xml_from_file(self.working_dir, harvester.OaiHarvesterFileNames.SETS.value)

        sets_items = xml.findall(".//{" + utils.xmlns.oai + "}" + "set")
        rsets = []
        for s in sets_items:
            setName = s.find(".//{" + utils.xmlns.oai + "}" + "setName").text
            term = Term.query.filter_by(vocabulary_id=self.voc.id, name=setName).first()
            if not term:
                term = Term()
                term.name = setName
                term.vocabulary_id = self.voc.id
                db.session.add(term)
        db.session.commit()

#  TODO: esta clase supone que la carpeta esta correctamente formada.
# lo que sigue debe ser funcion de la clase harvester, que es la que garantiza formar bien la carpeta.
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

        items = HarvestedItem.query.filter_by(repository_id=self.source.id).all()
        for item in items:
            try:
                # currently supporting dc elements and nlm (to get more info about authors)
                if item.status != HarvestedItemStatus.DELETED:
                # and item.status != HarvestedItemStatus.ERROR:
                    self.oai_dc = DubliCoreElements()
                    self.nlm = JournalPublishing()

                    dc = self._process_format(item, self.oai_dc)
                    if dc is not None:
                        nlm = None
                        if "nlm" in self.formats:
                            nlm = self._process_format(item, self.nlm)

                        data = self._crate_iroko_dict(item, dc, nlm)
                        # print(data)


                        record, status = IrokoRecord.create_or_update(
                            data, dbcommit=True, reindex=True
                        )
                        item.status = HarvestedItemStatus.RECORDED
                        item.record = record.id
                        print(item.record)
                    else:
                        print("dublin core is none, nothing to do: item: {0}".format(item.identifier))
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
            xml = utils.get_xml_from_file(self.working_dir, formater.getMetadataPrefix() + ".xml", extra_path=str(item.id))
            return formater.ProcessItem(xml)
        except Exception as e:
            # nothing to do...
            # TODO: if this is none try to collect this format again
            # (only one time, until the next global iteration over the source)
            return None


    def _crate_iroko_dict(self, item: HarvestedItem, dc, nlm=None):

        data = dict(dc)
        # print(str(data))
        if nlm is not None:
            data["creators"] = nlm["creators"]
            data["contributors"] = nlm["contributors"]


        data["source"] = {"uuid": str(self.source.uuid), "name": str(self.source.name)}
        spec_code = data["spec"]
        for s in self.repository.data['sets']:
            for k,v in s.items():
                if spec_code == k:
                    data["spec"] = {"code": k, "name": v}
        # aqui iria encontrar los tipos de colaboradores usando nlm...
        # tambien es posible hacer un request de los textos completos usando dc.relations

        self._update_item_data_vocabularies(data)

        data['status'] = self.source.source_status.value
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
        tuus = []
        for ts in self.source.term_sources:
            tuus.append(str(ts.term.uuid))

        rs_term = Term.query.filter_by(vocabulary_id=self.voc.id, name=data['spec']['name']).first()
        if rs_term:
            tuus.append(str(rs_term.uuid))
        data['iroko_terms'] = tuus


    def _udate_record_type(self, data):
        """ update or define a record_type, based on record_set
        record_set should have a record_type as a class
        if the record_set in the data has a record_type associated,
        then the corresponding record_type will be associated into the data.
        """
        pass

