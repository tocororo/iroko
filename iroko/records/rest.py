#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from flask import Blueprint, request

from iroko.api import IrokoAggs
from iroko.utils import IrokoResponseStatus, iroko_json_response

api_blueprint = Blueprint(
    'iroko_api_records',
    __name__,
    url_prefix='/records'
    )

