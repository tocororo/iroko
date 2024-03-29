#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Celery tasks used by Iroko-Harvester."""
from datetime import time

# from iroko.harvester.signals import harvest_finished
#
from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

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
def iroko_test_task():
    # time.sleep(50)
    for i in range(0, 10):
        pass
        logger.info('counting... {0} '.format(i))
        # print(str(i))

    return 10
#     # harvest_finished.send(source)
#     # source = Source.query.filter_by(id=source_id).first()
#     #     if source is not None:
#     #         harvester = OaiHarvester(source, work_remote=work_remote, request_wait_time=4)
#     #         harvester.identity_source()
#     #         harvester.discover_items()
#     #         harvester.process_items()
