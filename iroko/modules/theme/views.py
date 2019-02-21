# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 UPR.
#
# iroko is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.



"""iroko interface."""

from __future__ import absolute_import, print_function

from flask import Blueprint

blueprint = Blueprint(
    'iroko_theme',
    __name__,
    template_folder='templates',
    static_folder='static'
)
