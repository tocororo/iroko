
"""Celery tasks used by Iroko-Harvester."""

from __future__ import absolute_import, print_function

from celery import shared_task
from iroko.harvester.oai.harvester import OaiHarvester
from iroko.sources.models import Source
# from iroko.harvester.signals import harvest_finished
import time

@shared_task
def test_task(source):

    harvester = OaiHarvester(source)
    # iterator.get_identifiers()
    # iterator.get_all_metadata()

@shared_task
def harvest_source(source_id, work_remote=True, request_wait_time=3):
    source = Source.query.filter_by(id=source_id).first()
    for i in [0,1000000]:
        time.sleep(1)
        print(str(i))
    # harvest_finished.send(source)
    # source = Source.query.filter_by(id=source_id).first()
    #     if source is not None:
    #         harvester = OaiHarvester(source, work_remote=work_remote, request_wait_time=4)
    #         harvester.identity_source()
    #         harvester.discover_items()
    #         harvester.process_items()