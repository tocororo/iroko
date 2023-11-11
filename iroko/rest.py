#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from flask import Blueprint, request

from iroko.api import IrokoAggs
from iroko.utils import IrokoResponseStatus, iroko_json_response

#


api_blueprint = Blueprint(
    'iroko_api_utils',
    __name__,
    url_prefix='/utils'
    )

@api_blueprint.route('/agg/terms', methods=['POST'])
def get_aggregation():
    """endpoint para navegar por los terminos una agregacion, basado en un filro actual
        debe recibir un objeto con la siguiente estructura.
        example_query = {
            "index": "records",
            "filters": [
                {"key": "keywords", "value": ["Cuba", "Covid"]},
                {"key": "creators", "value": ["Rafael Pila Peláez"]}
                ],
            "agg": {
                "filter": "creators",
                "size": 10000,
                "start": 10,
                "end": 20
                }
            }
    """

    # try:

    if not request.is_json:
        raise Exception("No JSON data provided")

    query = request.json
    result = IrokoAggs.getAgg(query=query)
    if not result:
        raise Exception('No such field aggregation')

    return iroko_json_response(IrokoResponseStatus.SUCCESS, 'ok', 'terms', result)

    # except Exception as e:
    #     return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
