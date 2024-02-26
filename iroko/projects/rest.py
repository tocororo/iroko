

from __future__ import absolute_import, print_function

import datetime

import os
from uuid import UUID, uuid4

from flask import Blueprint, flash, jsonify, make_response, request, Response
from invenio_indexer.api import RecordIndexer
from marshmallow import ValidationError
from invenio_db import db
from iroko.pidstore import pids
from iroko.projects.api import ProjectRecord
from iroko.persons.fixtures import allowed_file, csv_to_json, get_ext
from iroko.persons.serializers import json_v1_response
from iroko.projects.marshmallow.json import ProjectMetadataSchemaV1

api_blueprint = Blueprint(
    'iroko_api_projects',
    __name__,
    url_prefix='/projects'
)


@api_blueprint.route('/pid', methods=['GET'])
def get_project_by_pid_canonical():
    try:
        _id = request.args.get('value')
        print("**********************", _id)
        pid, project = ProjectRecord.get_record(id_=_id)
        print(project, "hola")
        if not pid or not project:
            raise Exception('Not Found')

        return json_v1_response(pid, project)
    except Exception as e:
        print(e)
        return make_response(jsonify({
            "ERROR":"Pid Not Found"
        }),404)






@api_blueprint.route('/new', methods=['POST'])
def create_project():
    if not request.is_json:
        raise Exception("No se especifican datos en formato json para la curacion")
    try:
        data=request.get_json()
        projectData = ProjectMetadataSchemaV1().load(data['project'])
        res = ProjectRecord.create_project(data=projectData, org_uuid=uuid4())
        return res
    except ValidationError as err:
        return make_response(jsonify({
            "Error":err.messages,
        }),400)


@api_blueprint.route('/<uri>', methods=['DELETE'])
def delete_project(uri):
    try:
        pid,project =ProjectRecord.get_record_by_pid(record_pid_type=pids.PROJECT_PID_TYPE,pid_value=uri)
        if project is None:
            return make_response(jsonify({
                "Error":"Not found"
            }),404)
        project.delete()
        RecordIndexer().delete(project)
        db.session.commit()
        return make_response(jsonify({
            "Deleted":project,
        }),200)
    except Exception as err:
        return make_response(jsonify({
            "Error":str(err)
        }),400)





@api_blueprint.route('/import/', methods=['POST'])
# @require_api_auth()
def upload_file():

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
                ProjectRecord.load_from_json_file(json_path)
                response = make_response(jsonify({'msg': 'success'}))
                return response, 201
            else:
                filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.'+'json'
                file.save(os.path.join('./', filename))
                ProjectRecord.load_from_json_file(
                    os.path.join('./', filename))
                response = make_response(jsonify({'msg': 'success'}))
                return response, 201
        else:
            raise Exception("no valid file extension")

    # except Exception as e:
    #     print(e)
    #     return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)