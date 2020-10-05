
from __future__ import absolute_import, division, print_function

import traceback

import click
from flask import current_app
from flask.cli import with_appcontext

from iroko.harvester.api import PrimarySourceHarvester
from iroko.harvester.models import HarvestType, HarvestedItemStatus, Repository
from iroko.harvester.oai.harvester import OaiHarvester
# from iroko.documents.api import Document
from iroko.sources.models import Source


# from iroko.documents.dojson.dc import create_dict
# from iroko.oaiharvester.api import get_records, get_sets, get_records_dates
# from sickle import Sickle
# from sickle.oaiexceptions import BadArgument
# from .formats.dc import marshmallow
# from iroko.harvester.processors.oai.iterator import OaiIterator
# from iroko.harvester.processors.oai.formaters import DubliCoreElements

@click.group()
def harvester():
    """Command related to harevest iroko data."""


@harvester.command()
@with_appcontext
def rescan():
    """rescanea el directorio """
    harvest_dir = current_app.config['HARVESTER_DATA_DIRECTORY']

    # print("####################### start harvestig from dir")
    PrimarySourceHarvester.rescan_zip_files_in_dir(harvest_dir)

    # print("####################### start archiving")
    PrimarySourceHarvester.archive_zip_files_in_dir(harvest_dir)


@harvester.command()
@click.argument('zip_dir')
@with_appcontext
def archive_zip_dir(zip_dir):
    """rescanea el directorio y hace archive """
    PrimarySourceHarvester.archive_zip_files_in_dir(zip_dir)


@harvester.command("rescandir")
@click.argument('source_dir')
@with_appcontext
def rescan_dir(source_dir):
    """rescanea un source dir """
    PrimarySourceHarvester.rescan_zip_files_in_dir(source_dir)


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
        # print("Scheduled job {0}".format(job.id))




@harvester.command()
@with_appcontext
def harvestall():
    """harvest all sources with oai"""
    sources = Source.query.all()
    count = 0
    for source in sources:
        # print(source.uuid)
        repo = Repository.query.filter_by(source_id=source.id).first()
        # print(repo)
        if repo is not None and repo.harvest_type == HarvestType.OAI and \
            (repo.status is None or \
            repo.status == HarvestedItemStatus.ERROR):
            # print("{0} - {1} : {2} : {3}".format(count, source.id, source.name, repo.status))
            count = count + 1
            try:
                # print('###########################')
                # print("{0} - {1} - {2}".format(source.id, source.name, repo.status))
                # print("{0} - {1} - {2}".format(source.id, source.name, repo.harvest_endpoint))
                harvester = OaiHarvester(source, work_remote=True, request_wait_time=0)
                harvester.identity_source()
                harvester.discover_items()
            except Exception as e:
                print (e.__doc__)
            finally:
                # print("{0} - {1} - {2}".format(source.id, source.name, repo.status))
                # print('###########################')

