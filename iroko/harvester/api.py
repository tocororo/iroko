#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
import enum

from iroko.harvester.models import Repository


class Formatter(object):
    """ A Formatter will return a dict given something
    (xml, html, or something else) """

    def __init__(self):
        self.metadataPrefix = None

    def get_metadata_prefix(self):
        """name of the formatter oai_dc, nlm, jats"""
        return self.metadataPrefix

    def process_item(self, item):
        """given an item return a dict given an item"""
        raise NotImplementedError


class SourceHarvesterMode(enum.Enum):
    FILE_SYSTEM = "ERROR"
    REMOTE = "HARVESTED"


class Item:
    format = ''
    raw = ''
    data = {}


class BaseHarvester(object):
    """any harvester"""

    def process_pipeline(self):
        raise NotImplementedError


class SourceHarvester(BaseHarvester):
    """Harvester base class. Any harvester must implement process_repo method. """

    def __init__(self, repo: Repository):
        assert repo
        self.repo = repo

    def process_pipeline(self):
        raise NotImplementedError

