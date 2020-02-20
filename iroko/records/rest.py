
from flask import Blueprint, current_app, jsonify, request, json, render_template, flash, url_for, redirect
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.records.api import IrokoAggs

api_blueprint = Blueprint(
    'iroko_api_records',
    __name__,
    url_prefix='/records'
)


@api_blueprint.route('/aggs/<field>')
def get_aggregations(field):
    """return aggregation"""

    try:
        size = int(request.args.get('size')) if request.args.get('size') and int(request.args.get('size')) >=0 else 10

        result = IrokoAggs.getAggrs(field, size)
        if not result:
            raise Exception('No such field aggregation')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok','aggs', result)

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
