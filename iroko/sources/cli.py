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
def initjournals():
    """Init journals."""
    init_journals()


# @sources.command()
# @with_appcontext
# def initjournalsrelations():
#     """Init journals relations with terms."""
#     init_term_sources()
#


@sources.command()
@with_appcontext
def issncollect():
    """get all cuban issn from issn.org and create/update respective source versions"""
    IssnHarvesterManager.collect_issn()


@sources.command()
@with_appcontext
def issnsync():
    IssnHarvesterManager.sync_db()


@sources.command()
@with_appcontext
def issnsyncrecords():
    IssnHarvesterManager.sync_records()


@sources.command()
@with_appcontext
def miarcollectdb():
    """get all info from miar"""
    MiarHarvesterManager.collect_databases()

@sources.command()
@with_appcontext
def miarsyncdb():
    MiarHarvesterManager.sync_databases()


@sources.command()
@with_appcontext
def miarcollectjournals():
    MiarHarvesterManager.collect_journals()


@sources.command()
@with_appcontext
def miarsyncjournals():
    MiarHarvesterManager.sync_journals()





