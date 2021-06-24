#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import enum
from time import sleep

from iroko.sources.api import SourceRecord


class Item:
    format = ''
    raw = ''
    data = {}


class SourceHarvesterMode(enum.Enum):
    FILE_SYSTEM = "ERROR"
    REMOTE = "HARVESTED"


class BaseHarvester(object):
    """Clase base de todos los harvesters
    puede ser implementado para fuentes primarias y secundarias."""

    def process_pipeline(self):
        """Procesar el pipeline que define el harvester"""
        raise NotImplementedError


class SourceHarvester(BaseHarvester):
    """An iterator is responsible iterate over the items of a source, the OAI case is the most
    simple, in other case, is also responsible for discover the iterm before iterate over its"""

    def __init__(self, source: SourceRecord, work_remote=True, request_wait_time=3):
        self.work_remote = work_remote
        self.request_wait_time = request_wait_time
        self.source = source

    def identity_source(self):
        """ en oai esto significa identify, metadata formats, es decir, aqui se trata lo que
        tiene que ver con el source"""
        raise NotImplementedError

    def discover_items(self):
        """descubrir los items que tiene, en el caso de oai es el verbo getIdentifiers y
        posteriormente , se traen los datos, en el caso de oai, esto es traer para cada item
        todos los metadata formats y guardarlo como ficheros xml en el HARVESTER_DATA_DIRECTORY"""
        raise NotImplementedError

    def process_items(self):
        """ una vez descubiertos los items aqui se procesan y eventualmente se crea un record"""
        raise NotImplementedError

    def process_pipeline(self):
        self.identity_source()
        sleep(self.request_wait_time)
        self.discover_items()
        sleep(self.request_wait_time)
        self.process_items()


class Formater(object):
    """ A Formater will return a dict given something (xml, html, or something else) """

    def __init__(self):
        self.metadataPrefix = None

    def getMetadataPrefix(self):
        """name of the formater oai_dc, nlm, jats"""
        return self.metadataPrefix

    def ProcessItem(self, item):
        """given an item return a dict given an item"""
        raise NotImplementedError
