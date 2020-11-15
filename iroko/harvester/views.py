#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from __future__ import absolute_import, print_function

from flask import Blueprint

api_blueprint = Blueprint(
    'iroko_api_harvester',
    __name__
)
