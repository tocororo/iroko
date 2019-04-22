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

from iroko.modules.documents.api import Document
from iroko.modules.sources.models import Sources
from iroko.modules.documents.dojson.dc import create_dict
from iroko.modules.oaiharvester.api import get_records, get_sets, get_records_dates

from sickle import Sickle
from sickle.oaiexceptions import BadArgument

# from .formats.dc import marshmallow

@click.group()
def harvester():
    """Command related to harevest iroko data."""


@harvester.command()
@with_appcontext
def harvestall():
    """harvest all sources with oai"""

    # ids1 = ['oai:cfores.upr.edu.cu:article/82', \
    #     'oai:cfores.upr.edu.cu:article/329']

    ids = ['oai:ojs.pkp.sfu.ca:article/20']

    request, records = get_records(metadata_prefix='oai_dc',identifiers=ids, url="http://10.80.3.42/index.php/coodes/oai")

    # request, records = get_records(metadata_prefix='oai_dc',identifiers=ids, url="http://10.80.4.42/index.php/cfores/oai")

    for record in records:
        # print(record.metadata['date'][0])
        source = '2c924b47-5cc4-402a-807e-0b86b1eb04e5'
        # marshmallow.parse(record)
        # print(record.metadata['description']['es-ES'])
        # data = create_dict(record, source)
        # # print(data)
        # record, status = Document.create_or_update(
        #     data, vendor=source, dbcommit=True, reindex=True
        # )
        # click.echo('record uuid: ' + str(record.id) + ' | ' + status)

def some():    
    count = 0
    sources = Sources.query.all()
    for source in sources:
        if source.havest_endpoint:
            print(source.havest_endpoint)
            uuid = source.uuid
            url = source.havest_endpoint
            for year in range(2001, 2019):
                request, records = get_records_dates(   \
                    url=url, \
                    from_date=date(year, 1, 1), \
                    until_date=date(year, 12, 31))
                ids = []
                for rec in records:
                    count+= 1
                    ids.append(rec.header.identifier)
                try:
                    print(ids)
                    req, recs = get_records(identifiers=ids, url=url)
                    for recfull in recs:
                        data = create_dict(recfull, uuid)
                        record, status = Document.create_or_update( \
                                data, vendor=uuid, dbcommit=True, reindex=True)
                        click.echo('record uuid: ' + str(record.id) + ' | ' + status)
                except BadArgument:
                    continue

    # sets = get_sets(url)
    # sickle = Sickle(url)
    # iterator = sickle.ListRecords(metadataPrefix='oai_dc')
    
    # for record_set in iterator:
    #     count += 1
    #     print(iterator.resumption_token)
    print(count)

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