

from __future__ import absolute_import, print_function

import datetime
from math import e
import os
from urllib import response
from uuid import UUID, uuid4

from flask import Blueprint, flash, jsonify, make_response, request

from iroko.projects.api import ProjectRecord
from iroko.persons.fixtures import allowed_file, csv_to_json, get_ext
from iroko.persons.serializers import json_v1_response
from iroko.pidstore import pids
from iroko.projects.marshmallow.json import projectMetadataSchema

api_blueprint = Blueprint(
    'iroko_api_projects',
    __name__,
    url_prefix='/projects'
)


@api_blueprint.route('/pid', methods=['GET'])
def get_person_by_pid_canonical():
    """
    Get a source by any PID received as a argument, including UUID
    this method gives the directed organization with that pid, even if is obsolete or redirected status
    """
    try:
        _id = request.args.get('value')
        print("**********************", _id)
        pid, project = ProjectRecord.get_record_by_pid(
            pids.PROJECT_PID_TYPE, _id)
        if not pid or not project:
            raise Exception('')

        return json_v1_response(pid, project)

    except Exception as e:
        return jsonify({
            'ERROR': 'no pid found'.format(_id)
        })


@api_blueprint.route('/', methods=['GET'])
def get_projects():
    list = ProjectRecord.get_records(['*'])
    return list


@api_blueprint.route('/new', methods=['POST'])
def get_hello_world():
    data = request.get_json()
    res = ProjectRecord.create_project(data=data, org_uuid=uuid4())
    return res


@api_blueprint.route('/import/<org_uuid>', methods=['POST'])
# @require_api_auth()
def upload_file(org_uuid):
    # /tmp/iroko/person/<datetime>.[csv|json]
    # try:
    if request.method == 'POST':
        print(request.__dict__)
        print('--------------------------------')
        print(request.files)
        print('--------------------------------')
        if 'file' not in request.files:
            flash('No file part')
            raise Exception("No file part")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            raise Exception("Not file in request")
        if file and allowed_file(file.filename):
            if 'csv' == get_ext(file.filename):
                json_path = csv_to_json(file)
                ProjectRecord.load_from_json_file(json_path, org_uuid)
                response = make_response(jsonify({'msg': 'success'}))
                return response, 201
            else:
                filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.'+'json'

                file.save(os.path.join('./data', filename))
                ProjectRecord.load_from_json_file(
                    os.path.join('./data', filename), org_uuid)
                response = make_response(jsonify({'msg': 'success'}))
                return response, 201
        else:
            raise Exception("no valid file extension")

    # except Exception as e:
    #     print(e)
    #     return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
