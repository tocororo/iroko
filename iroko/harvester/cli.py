
from __future__ import absolute_import, division, print_function

import click
import sys
from datetime import date

from flask.cli import with_appcontext
import traceback

# from iroko.documents.api import Document
from iroko.sources.models import Source
from iroko.harvester.models import HarvestType, HarvestedItemStatus
# from iroko.documents.dojson.dc import create_dict
# from iroko.oaiharvester.api import get_records, get_sets, get_records_dates

# from sickle import Sickle
# from sickle.oaiexceptions import BadArgument

# from .formats.dc import marshmallow

# from iroko.harvester.processors.oai.iterator import OaiIterator
# from iroko.harvester.processors.oai.formaters import DubliCoreElements

from iroko.harvester.oai.harvester import OaiHarvester

from iroko.harvester.api import PrimarySourceHarvester, SecundarySourceHarvester
from iroko.harvester.tasks import harvest_source_task

from invenio_db import db

@click.group()
def harvester():
    """Command related to harevest iroko data."""

@harvester.command()
@with_appcontext
def rescan():
    """rescanea el directorio """
    PrimarySourceHarvester.rescan_and_fix_harvest_dir()

@harvester.command("rescandir")
@click.argument('source_dir')
@with_appcontext
def rescan_dir(source_dir):
    """rescanea un source dir """
    PrimarySourceHarvester.rescan_and_fix_source_dir(source_dir)


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
        PrimarySourceHarvester.harvest_pipeline(sid, work_remote=True, step=st)
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
        if source is not None and source.repository.status is None or source.repository.status == HarvestedItemStatus.ERROR:
            print("{0} - {1} : {2} : {3}".format(count, source.id, source.name, source.repository.status))
            count = count + 1
            try:
                print('###########################')
                print("{0} - {1} - {2}".format(source.id, source.name, source.repository.status))
                print("{0} - {1} - {2}".format(source.id, source.name, source.repository.harvest_endpoint))
                harvester = OaiHarvester(source, work_remote=True, request_wait_time=0)
                harvester.identity_source()
                harvester.discover_items()
            except Exception as e:
                print (e.__doc__)
            finally:
                print("{0} - {1} - {2}".format(source.id, source.name, source.repository.status))
                print('###########################')

@harvester.command()
@click.option('-ri', '--remoteissns', required=False, type=bool)
@click.option('-rf', '--remoteinfo', required=False, type=bool)
@click.option('-i', '--info', required=False, type=bool)
@with_appcontext
def issn(remoteissns, remoteinfo, info):
    """get all cuban issn from issn.org and create/update respective source versions"""
    SecundarySourceHarvester.process_issn(remoteissns, remoteinfo, info)


@harvester.command()
@click.option('-rc', '--recheck', required=False, type=bool)
@with_appcontext
def miar(recheck):
    """get all info from miar"""
    SecundarySourceHarvester.harvest_miar(recheck)
