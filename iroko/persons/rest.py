


from __future__ import absolute_import, print_function


from flask import Blueprint, request, jsonify, abort, current_app

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
        pid, org = PersonRecord.get_record_by_pid(pids.PERSON_PID_TYPE, _id)
        if not pid or not org:
            raise Exception('')

        return json_v1_response(pid, org)

    except Exception as e:
        return jsonify({
            'ERROR': 'no pid found'.format(_id)
        })

