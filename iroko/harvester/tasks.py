#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Celery tasks used by Iroko-Harvester."""

from __future__ import absolute_import, print_function

# from iroko.harvester.signals import harvest_finished
#
# @shared_task
# def test_task(source):
#     pass
#     # harvester = OaiHarvester(source)
#     # iterator.get_identifiers()
#     # iterator.get_all_metadata()
#
# @shared_task
# def harvest_source_task(source_id, work_remote=True, request_wait_time=3):
#     pass
#     # source = Source.query.filter_by(id=source_id).first()
#     # for i in [0,1000000]:
#     #     pass
#         # print(str(i))
#     # harvest_finished.send(source)
#     # source = Source.query.filter_by(id=source_id).first()
#     #     if source is not None:
#     #         harvester = OaiHarvester(source, work_remote=work_remote, request_wait_time=4)
#     #         harvester.identity_source()
#     #         harvester.discover_items()
#     #         harvester.process_items()
