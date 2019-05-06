
"""Celery tasks used by Iroko-Harvester."""

from __future__ import absolute_import, print_function

from celery import shared_task 
from iroko.harvester.oai.harvester import OaiHarvester


@shared_task
def test_task(source):

    harvester = OaiHarvester(source)
    # iterator.get_identifiers()
    # iterator.get_all_metadata()
