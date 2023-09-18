


from __future__ import absolute_import, print_function

import datetime
import os

from flask import Blueprint, flash, jsonify, make_response, request

from iroko.patents.api import PatentRecord
from iroko.patents.fixtures import allowed_file, csv_to_json, get_ext
from iroko.patents.serializers import json_v1_response
from iroko.pidstore import pids

api_blueprint = Blueprint(
    'iroko_api_patents',
    __name__,
    url_prefix='/patents'
    )


@api_blueprint.route('/pid', methods=['GET'])
def get_patent_by_pid_canonical():
    """
    Get a source by any PID received as an argument, including UUID
    this method gives the directed organization with that pid, even if is obsolete or redirected status
    """
    try:
        _id = request.args.get('value')
        print("**********************", _id)
        pid, patent = PatentRecord.get_record_by_pid(pids.PATENT_PID_TYPE, _id)
        if not pid or not patent:
            raise Exception('')

        return json_v1_response(pid, patent)

    except Exception as e:
        return jsonify({
            'ERROR': 'no pid found'.format(_id)
        })






@api_blueprint.route('/import/<org_uuid>', methods=['POST'])
# @require_api_auth()
def upload_file(per_uuid):
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
            if 'csv'==get_ext(file.filename):
                json_path=csv_to_json(file)
                PatentRecord.load_from_json_file(json_path, per_uuid)
                response = make_response(jsonify({'msg': 'success'}))
                return response, 201
            else:
                filename=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.'+'json'

                file.save(os.path.join('./data', filename ))
                PatentRecord.load_from_json_file(os.path.join('./data',filename),per_uuid )
                response = make_response(jsonify({'msg': 'success'}))
                return response ,201
        else:
            raise Exception("no valid file extension")

    # except Exception as e:
    #     print(e)
    #     return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
