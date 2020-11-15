#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, division, print_function

import click
from flask.cli import with_appcontext

from iroko.sources.fixtures import init_journals
from iroko.sources.harvesters.issn import IssnHarvesterManager
from iroko.sources.harvesters.miar import MiarHarvesterManager


@click.group()
def sources():
    """Command related to Iroko Sources iroko data."""


@sources.command()
@with_appcontext
def sync_old_journals_data():
    """sync journal data from old tocororo website"""
    init_journals()


# @sources.command()
# @with_appcontext
# def initjournalsrelations():
#     """Init journals relations with terms."""
#     init_term_sources()
#


@sources.command()
@with_appcontext
def issn_collect():
    """get all cuban issn from issn.org save to file"""
    IssnHarvesterManager.collect_issn()


@sources.command()
@with_appcontext
def issn_sync_db():
    """save all collected issn.org to SourceRawData and collect missing data if any"""
    IssnHarvesterManager.sync_db()


@sources.command()
@with_appcontext
def issn_sync_records():
    """parse SourceRawData and sync to SourceRecords """
    IssnHarvesterManager.sync_records()


@sources.command()
@with_appcontext
def miar_collect_db():
    """get all miar databases, save to file"""
    MiarHarvesterManager.collect_databases()


@sources.command()
@with_appcontext
def miar_sync_db():
    """create with collected miar databases a Vocabulary """
    MiarHarvesterManager.sync_databases()


@sources.command()
@with_appcontext
def miar_collect_journals():
    """collect miar info from all SourceRawData, save to files"""
    MiarHarvesterManager.collect_journals()


@sources.command()
@with_appcontext
def miar_sync_journals():
    """sync to SourceRawData all collected info"""
    MiarHarvesterManager.sync_journals()


@sources.command()
@with_appcontext
def miar_sync_records():
    """parse SourceRawData and sync to SourceRecords"""
    MiarHarvesterManager.sync_journals_records()
