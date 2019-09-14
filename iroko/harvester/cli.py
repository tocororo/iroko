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
import sys
from datetime import date

from flask.cli import with_appcontext
import traceback

# from iroko.documents.api import Document
from iroko.sources.models import Source, HarvestType, RepositoryStatus
# from iroko.documents.dojson.dc import create_dict
# from iroko.oaiharvester.api import get_records, get_sets, get_records_dates

# from sickle import Sickle
# from sickle.oaiexceptions import BadArgument

# from .formats.dc import marshmallow

# from iroko.harvester.processors.oai.iterator import OaiIterator
# from iroko.harvester.processors.oai.formaters import DubliCoreElements

from iroko.harvester.oai.harvester import OaiHarvester

from iroko.harvester.api import Harvester
from iroko.harvester.tasks import harvest_source

from invenio_db import db

@click.group()
def harvester():
    """Command related to harevest iroko data."""

@harvester.command()
@with_appcontext
def rescan():
    """rescanea el directorio """
    Harvester.rescan_and_fix_harvest_dir()

@harvester.command("rescandir")
@click.argument('source_dir')
@with_appcontext
def rescan_dir(source_dir):
    """rescanea un source dir """
    Harvester.rescan_and_fix_source_dir(source_dir)


@harvester.command("harvestsource")
@click.option('-s', '--step')
@click.argument('source_id')
@with_appcontext
def harvest_source(source_id, step=0):
    """harvest source
    -s = 0 start harvest in harvester.identity_source()
    -s = 1 start harvest in harvester.discover_items()
    -s = 2 start harvest in harvester.process_items()
    """
    try:
        sid = int(source_id)
        st = int(step)
        Harvester.harvest_pipeline(sid, work_remote=True, step=st)
    except Exception:
        traceback.format_exc()



@harvester.command()
@with_appcontext
def testcelery():
    sources = Source.query.all()
    for source in sources:
        job = harvest_source.delay(source.id, work_remote=True, request_wait_time=3)
        print("Scheduled job {0}".format(job.id))




@harvester.command()
@with_appcontext
def harvestall():
    """harvest all sources with oai"""
    sources = Source.query.filter_by(repo_harvest_type=HarvestType.OAI).all()
    count = 0
    for source in sources:
        if source is not None and source.repo_status is None or source.repo_status == RepositoryStatus.ERROR:
            print("{0} - {1} : {2} : {3}".format(count, source.id, source.name, source.repo_status))
            count = count + 1
            try:
                print('###########################')
                print("{0} - {1} - {2}".format(source.id, source.name, source.repo_status))
                print("{0} - {1} - {2}".format(source.id, source.name, source.repo_harvest_endpoint))
                harvester = OaiHarvester(source, work_remote=True, request_wait_time=0)
                harvester.identity_source()
                harvester.discover_items()
            except Exception as e:
                print (e.__doc__)
            finally:
                print("{0} - {1} - {2}".format(source.id, source.name, source.repo_status))
                print('###########################')

            # harvester.process_items()
    # count = 1
    # for source in sources:
    #     print(source.harvest_endpoint)
    #     try:
    #         iterator = OaiIterator(None, source,  init_directory=True,max_retries=2)
    #         iterator.get_identifiers()
    #         iterator.get_all_metadata()
    #         count+=1
    #     except Exception as e:
    #         print (e.__doc__)
    # print("def harvestall():"+str(count))

@harvester.command()
@with_appcontext
def preprocess_items():
    print('preprocess_items():')


#     # ids1 = ['oai:cfores.upr.edu.cu:article/82', \
#     #     'oai:cfores.upr.edu.cu:article/329']

#     ids = ['oai:ojs.pkp.sfu.ca:article/20']

#     request, records = get_records(metadata_prefix='oai_dc',identifiers=ids, url="http://10.80.3.42/index.php/coodes/oai")

#     # request, records = get_records(metadata_prefix='oai_dc',identifiers=ids, url="http://10.80.4.42/index.php/cfores/oai")

#     for record in records:
#         # print(record.metadata['date'][0])
#         source = '2c924b47-5cc4-402a-807e-0b86b1eb04e5'
#         # marshmallow.parse(record)
#         # print(record.metadata['description']['es-ES'])
#         # data = create_dict(record, source)
#         # # print(data)
#         # record, status = Document.create_or_update(
#         #     data, vendor=source, dbcommit=True, reindex=True
#         # )
#         # click.echo('record uuid: ' + str(record.id) + ' | ' + status)

# def some():
#     count = 0
#     sources = Source.query.all()
    # for source in sources:
    #     if source.havest_endpoint:
    #         print(source.havest_endpoint)
    #         uuid = source.uuid
    #         url = source.havest_endpoint
    #         for year in range(2001, 2019):
    #             request, records = get_records_dates(   \
    #                 url=url, \
    #                 from_date=date(year, 1, 1), \
    #                 until_date=date(year, 12, 31))
    #             ids = []
    #             for rec in records:
    #                 count+= 1
    #                 ids.append(rec.header.identifier)
    #             try:
    #                 print(ids)
    #                 req, recs = get_records(identifiers=ids, url=url)
    #                 for recfull in recs:
    #                     data = create_dict(recfull, uuid)
    #                     record, status = Document.create_or_update( \
    #                             data, vendor=uuid, dbcommit=True, reindex=True)
    #                     click.echo('record uuid: ' + str(record.id) + ' | ' + status)
    #             except BadArgument:
    #                 continue

    # sets = get_sets(url)
    # sickle = Sickle(url)
    # iterator = sickle.ListRecords(metadataPrefix='oai_dc')

    # for record_set in iterator:
    #     count += 1
    #     print(iterator.resumption_token)
#     print(count)

    # for s in request.ListSets():
    #     print(s)


    # request, records = get_records(identifiers=["oai:cfores.upr.edu.cu:article/123", url="http://192.168.56.7/index.php/cfores/oai")
    # for record in records:
    #     # print(record.metadata['date'][0])
    #     source = '2c924b47-5cc4-402a-807e-0b86b1eb04e5'
    #     data = create_dict(record, source)
    #     # print(data)
    #     record, status = Document.create_or_update(
    #         data, vendor=source, dbcommit=True, reindex=True
    #     )
    #     click.echo('record uuid: ' + str(record.id) + ' | ' + status)

# def get_sets(url ):
#     sets = get_sets(url)
#     for s in sets:
#         print(s)
