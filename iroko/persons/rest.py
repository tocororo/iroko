


from __future__ import absolute_import, print_function

from iroko.persons.fixtures import allowed_file
from flask import Blueprint, request, jsonify, abort, current_app, Flask, flash, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from iroko.persons.api import PersonRecord
from iroko.persons.serializers import json_v1_response
from iroko.pidstore import pids

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






@api_blueprint.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return 'Not file in request'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return 'Not file in request'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #Logical algorithm here
            response = make_response(jsonify({'msg': 'success'}))
            return response, 201
    return "Not suppoted file"
