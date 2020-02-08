from os import path, mkdir, listdir

from zipfile import ZipFile

from time import sleep

import traceback

import shutil

from lxml import etree

from sickle import Sickle

from flask import current_app

from invenio_db import db

from iroko.sources.models import Source

from iroko.harvester.models import HarvestedItem, HarvestedItemStatus, Repository

from iroko.harvester.oai import nsmap, request_headers
from iroko.harvester.oai.formaters import DubliCoreElements, JournalPublishing
from iroko.harvester.errors import IrokoHarvesterError
import iroko.harvester.utils as utils

import iroko.harvester.oai.harvester as harvester

from iroko.taxonomy.models import Term, Vocabulary

# PAra que la consola haga autoreaload
# In [1]: %load_ext autoreload

# In [2]: %autoreload 2


class Archivist:
    """
    Recibe un source
    - busca en el data dir el zip asociado
    - lo expande en tmp dir

    - se encarga de trabajar con los HarvestedItems, 
        - tomar lo que hay en los ficheros
    """

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

        self.working_dir = (
            current_app.config["IROKO_TEMP_DIRECTORY"]
            + "/iroko-harvest-"
            + str(self.source.uuid)
        )
        shutil.rmtree(self.working_dir, ignore_errors=True)

        zip_path = (
            current_app.config["HARVESTER_DATA_DIRECTORY"]
            + "/"
            + str(self.source.uuid)
            + ".zip"
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

        # TODO add adminEmail field to source data.. if nothing is set in the current Source.data...

        return name == self.source.name and oai_url == self.repository.harvest_endpoint and identifier == self.repository.identifier


    def _fix_repository_data_field(self):
        """
        replace the repository.data field with formats and sets of the OAI protocol
        """

        source_data = dict(self.source.data)
        repo_data = dict(self.repository.data)

        xml = utils.get_xml_from_file(self.working_dir, harvester.OaiHarvesterFileNames.FORMATS.value)
        formats = utils.get_multiple_elements(
                xml, "metadataPrefix", xmlns=utils.xmlns.oai
            )
        repo_data['formats'] = formats

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
        voc = Vocabulary.query.filter_by(name='record_sets').first()

        xml = utils.get_xml_from_file(self.working_dir, harvester.OaiHarvesterFileNames.SETS.value)

        sets_items = xml.findall(".//{" + utils.xmlns.oai + "}" + "set")
        rsets = []
        for s in sets_items:
            setName = s.find(".//{" + utils.xmlns.oai + "}" + "setName").text
            term = Term.query.filter_by(vocabulary_id=voc.id, name=setName).first()
            if not term:
                term = Term()
                term.name = setName
                term.vocabulary_id = voc.id
                db.session.add(term)
        db.session.commit()