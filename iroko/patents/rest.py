


from __future__ import absolute_import, print_function

from datetime import datetime
import json
import os

from flask import Blueprint, flash, jsonify, make_response, request
from elasticsearch.exceptions import NotFoundError
from invenio_pidstore.resolver import Resolver
from invenio_pidstore.models import PersistentIdentifier
from invenio_indexer.api import RecordIndexer
from flask_login import current_user
from invenio_oauth2server import require_api_auth
from invenio_db import db
from iroko.utils import remove_nulls

from iroko.patents.register.model import Register
from iroko.patents.register.marshmallow import register_schema, register_schema_many
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
def upload_file():
    try:
        if not request.is_json:
            raise Exception("No JSON data provided")


        input_data = request.json
        # patents = json.load(input_data, object_hook=remove_nulls)
        # print('patents',patents)
        a = 0
        for data in input_data:
            print(data)
            a = a + 1
            patent = PatentRecord(data)
            print(patent)
            patentRecord = None
            patentRecord, msg = PatentRecord.resolve_and_update(data=patent)
            print(patentRecord)
            if not patentRecord:
                print("no pids found, creating patent")
                patentRecord = PatentRecord.create(patent, iroko_pid_type=pids.PATENT_PID_TYPE)
                msg = 'created'

            return jsonify({
            'SUCCES':"Patentes creadas",
            'message':msg,
            })

    except Exception as e:
        return jsonify({
            'ERROR': str(e),
        })


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

@api_blueprint.route('/register', methods=['GET'])
def get_register():
    try:
        count = int(request.args.get('size')) if request.args.get('size') else 10
        page = int(request.args.get('page')) if request.args.get('page') else 1

        if page < 1:
            page = 1
        offset = count * (page - 1)
        limit = offset + count

        result = Register.query.all()
        total = len(result)

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            'ok', 'register', \
            {
                'data': register_schema_many.dump(result[offset:limit]),
                'total': total
                }
            )

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)

@api_blueprint.route('/register/new', methods=['POST'])
def create_register():
    try:
        input_data = request.json
        register = Register()
        register.data = input_data
        register.userEmail = input_data.get("userEmail")
        register.date = datetime.now()
        register.patents = input_data.get("patents")

        db.session.add(register)
        db.session.commit()

        msg = "New Register Created"

    except Exception as e:
        msg = str(e)
        return iroko_json_response(IrokoResponseStatus.ERROR, msg, None, None)

    return iroko_json_response(
        IrokoResponseStatus.SUCCESS, \
        msg, 'register', \
        register_schema.dump(register)
    )

@api_blueprint.route('/register/delete/<id>', methods=['DELETE'])
def delete_register(id):
    register = Register.query.filter_by(id = id).delete()
    db.session.commit()

    return make_response("Eliminado", 204)



