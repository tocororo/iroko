
"""Celery tasks used by Iroko-Harvester."""

from __future__ import absolute_import, print_function

from celery import shared_task 
from iroko.harvester.processors.oai import OaiIterator


@shared_task
def test_task(source):

    iterator = OaiIterator(None, source)
    iterator.get_identifiers()
    iterator.get_all_metadata()
