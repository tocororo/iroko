#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from __future__ import absolute_import, print_function

import datetime

from flask import Blueprint, request
from invenio_oauth2server import require_api_auth
from iroko.harvester.decorators import require_harvester_permission
from iroko.harvester.models import Repository
from iroko.harvester.oai.harvester import OaiHarvester
from iroko.harvester.tasks import HarvestersTaskManager
from iroko.sources.api import SourceRecord
from iroko.utils import IrokoResponseStatus, iroko_json_response

api_blueprint = Blueprint(
    'iroko_api_harvester',
    __name__,
    url_prefix='/harvester'
    )


@api_blueprint.route('/list/<status>', methods=['GET'])
@require_api_auth()
@require_harvester_permission()
def list_repositories(status):
    """
    list repositories
    status: ALL, ERROR, FETCHING, HARVESTED, RECORDED
    """
    try:
        if status == '' or status == 'ALL':
            status = None
        # TODO: repositories
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, 'ok', 'repositories', None
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/<uuid>/status', methods=['GET'])
@require_api_auth()
@require_harvester_permission()
def repo_status(uuid):
    """
    get the status of a repository
    params:
    uuid: Source uuid
    """
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')
        repository = Repository.query.filter_by(source_uuid=source.id).first()
        if not repository:
            raise Exception('Not repository found')
        # TODO: get all the process info of the record
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, 'ok', 'repositories', None
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)


@api_blueprint.route('/<uuid>/schedule', methods=['POST'])
@require_api_auth()
@require_harvester_permission()
def repo_schedule_harvest(uuid):
    """
    schedule a harvest of a source
    params:
    uuid: Source uuid
    """
    try:
        source = SourceRecord.get_record(uuid)
        if not source:
            raise Exception('Not source found')
        repository = Repository.query.filter_by(source_uuid=source.id).first()
        if not repository:
            raise Exception('Not repository found')
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json

        schedule_datetime = datetime.datetime.now()
        if 'datetime' in input_data:
            schedule_datetime = input_data['datetime']

        harvester_class = 'iroko.harvester.oai.harvester.OaiHarvester'
        if 'harvester_class' in input_data:
            harvester_class = input_data['harvester_class']
        # TODO: how instantiate an object from a class name.
        oai_harvester = OaiHarvester(repository)
        HarvestersTaskManager.schedule_harvest(oai_harvester, schedule_datetime)

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, 'ok', 'repositories', None
            )
    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)

