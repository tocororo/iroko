#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Celery tasks used by Iroko-Harvester."""

# from iroko.harvester.signals import harvest_finished
#
from celery import shared_task

from iroko.harvester.api import BaseHarvester


class HarvestersTaskManager(object):
    """Harvesters Manager"""

    @staticmethod
    def schedule_harvest(harvester: BaseHarvester, schedule_datetime):
        """"""
        # TODO: set this in a celery task at schedule_datetime
        celery_kwargs = {
            'kwargs': {
                'harvester': harvester,
                'queue': 'iroko',
                }
            }
        task_process_pipeline.apply_async(**celery_kwargs)
        # harvester.process_pipeline()
        # return None


@shared_task(ignore_result=True)
def task_process_pipeline(harvester: BaseHarvester):
    harvester.process_pipeline()


#
@shared_task(ignore_result=True)
def iroko_test_task(upto):
    for i in [0, upto]:
        pass
        print(str(i))
#     # harvest_finished.send(source)
#     # source = Source.query.filter_by(id=source_id).first()
#     #     if source is not None:
#     #         harvester = OaiHarvester(source, work_remote=work_remote, request_wait_time=4)
#     #         harvester.identity_source()
#     #         harvester.discover_items()
#     #         harvester.process_items()
