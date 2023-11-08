#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from flask import Blueprint, request

from iroko.records.api import IrokoAggs
from iroko.utils import IrokoResponseStatus, iroko_json_response

api_blueprint = Blueprint(
    'iroko_api_records',
    __name__,
    url_prefix='/records'
    )


@api_blueprint.route('/aggs/<field>')
def get_aggregations(field):
    """return aggregation"""

    try:
        size = int(request.args.get('size')) if request.args.get('size') and int(
            request.args.get('size')
            ) >= 0 else 10

        result = IrokoAggs.getAggrs(field, size)
        if not result:
            raise Exception('No such field aggregation')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok', 'aggs', result)

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
