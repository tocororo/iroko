


from __future__ import absolute_import, print_function
import os
import datetime
from iroko.persons.fixtures import allowed_file, csv_to_json, get_ext
from flask import Blueprint, request, jsonify, abort, current_app, Flask, flash, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from iroko.persons.api import PersonRecord
from iroko.persons.serializers import json_v1_response
from iroko.pidstore import pids
from invenio_oauth2server import require_api_auth

from iroko.utils import IrokoResponseStatus, iroko_json_response

api_blueprint = Blueprint(
    'iroko_api_persons',
    __name__,
    url_prefix='/persons'
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
        pid, person = PersonRecord.get_record_by_pid(pids.PERSON_PID_TYPE, _id)
        if not pid or not person:
            raise Exception('')

        return json_v1_response(pid, person)

    except Exception as e:
        return jsonify({
            'ERROR': 'no pid found'.format(_id)
        })






@api_blueprint.route('/import/<org_uuid>', methods=['POST'])
@require_api_auth()
def upload_file(org_uuid):
    # /tmp/iroko/person/<datetime>.[csv|json]
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                raise Exception("Not file in request")
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                raise Exception("Not file in request")
            if file and allowed_file(file.filename):
                if 'csv'==get_ext(file.filename):
                 json_path=csv_to_json(file)
                 PersonRecord.load_from_json_file(json_path, org_uuid)
                 response = make_response(jsonify({'msg': 'success'}))
                 return response, 201
                else:
                    filename=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.'+'json'

                    file.save(os.path.join('./data', filename ))
                    PersonRecord.load_from_json_file(os.path.join('./data',filename),org_uuid )
                    response = make_response(jsonify({'msg': 'success'}))
                    return response ,201

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
