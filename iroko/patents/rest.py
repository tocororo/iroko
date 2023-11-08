


from __future__ import absolute_import, print_function

import datetime
import os

from flask import Blueprint, flash, jsonify, make_response, request
from elasticsearch.exceptions import NotFoundError
from invenio_pidstore.resolver import Resolver
from invenio_pidstore.models import PersistentIdentifier
from invenio_indexer.api import RecordIndexer
from flask_login import current_user
from invenio_oauth2server import require_api_auth

from iroko.patents.api import PatentRecord
from iroko.patents.fixtures import allowed_file, csv_to_json, get_ext
from iroko.patents.serializers import json_v1_response
from iroko.pidstore import pids
from iroko.utils import IrokoResponseStatus, iroko_json_response
from iroko.pidstore.pids import (
    IDENTIFIERS_FIELD_TYPE, IROKO_OBJECT_TYPE, PATENT_PID_TYPE, identifiers_schemas,
    )

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
        pid, patent = PatentRecord.get_pat_by_pid(pids.PATENT_PID_TYPE, _id)
        if not pid or not patent:
            raise Exception('')

        return json_v1_response(pid, patent)

    except Exception as e:
        return jsonify({
            'ERROR': 'no pid found'.format(_id)
        })


@api_blueprint.route('/import', methods=['POST'])
# @require_api_auth()
def upload_file():
    # /tmp/iroko/person/<datetime>.[csv|json]
    # try:
    if request.method == 'POST':
        print(request.__dict__)
        print('--------------------------------')
        print(request.files)
        # print('--------------------------------')
        # if 'file' not in request.files:
        #     flash('No file part')
        #     raise Exception("No file part")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            raise Exception("Not file in request")
        if file and allowed_file(file.filename):
            if 'csv'==get_ext(file.filename):
                json_path=csv_to_json(file)
                PatentRecord.load_from_json_file(json_path)
                response = make_response(jsonify({'msg': 'success'}))
                return response, 201
            else:
                filename=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.'+'json'

                file.save(os.path.join('./data', filename ))
                PatentRecord.load_from_json_file(os.path.join('./data',filename))
                response = make_response(jsonify({'msg': 'success'}))
                return response ,201
        else:
            raise Exception("no valid file extension")

    # except Exception as e:
    #     print(e)
    #     return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)

@api_blueprint.route('/<uuid>/edit', methods=['POST'])
def edit_patent(uuid):
    """
    Dado un uuid modificar los datos de una patente
    """
    try:
        if not request.is_json:
            raise Exception("No se especifican datos en formato json para la curacion")
        input_data = request.json
        print("//////////////////////////////////////////////////////")
        print(input_data)
        print("///////////////////////////////////////////////////////")
        # org = org_json_v1.transform_record(input_data["id"], input_data)
        print("-------------------------------------------------------------")


        print("------------------------------------------------------------")

        pat, msg = PatentRecord.resolve_and_update(uuid, input_data)

        if not pat:
            raise Exception("No se encontro record de patente")

        print("entra a la api de editar patentes...........................................")
        return jsonify({
            'SUCCES':"Patente modificada",
            'message':msg,
            'org':pat
        })
    except Exception as e:
        print(e)
        return jsonify({
            'ERROR': str(e),
        })

@api_blueprint.route('/new', methods=['POST'])
def create_patent():
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")

        input_data = request.json
        pat= PatentRecord.create(input_data, iroko_pid_type=pids.PATENT_PID_TYPE)
        msg = 'ok'


        return jsonify({
            'SUCCES':"Patente creada",
            'message':msg,
            'pat':pat
        })

    except Exception as e:
        return jsonify({
            'ERROR HOLA': str(e),
        })

@api_blueprint.route('/delete/<uuid>', methods=['DELETE'])
def delete_patent(uuid):

    record = PatentRecord.get_record_by_pid_value(uuid)

    if not record:
        raise Exception("No se encontro record de patente")

    result = super(PatentRecord, record).delete(force=False)
    # if delindex:
    try:
        RecordIndexer().delete(record)
    except NotFoundError:
        pass


    return result
