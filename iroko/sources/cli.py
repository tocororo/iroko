# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Manage fixtures for INSPIRE site."""

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




