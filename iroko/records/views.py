# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 UPR.
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Blueprint definitions."""

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template

from iroko.sources.api import Sources
from iroko.taxonomy.api import Terms

blueprint = Blueprint(
    'iroko_records',
    __name__,
    template_folder='templates',
    static_folder='static',
)
"""Blueprint used for loading templates and static assets

The sole purpose of this blueprint is to ensure that Invenio can find the
templates and static files located in the folders of the same names next to
this file.
"""

def iroko_record_view(pid, record, template=None):

    source = Sources.get_source_by_id(uuid= record['source']['uuid'])
    terms = Terms.get_terms_by_uuid_list(record['iroko_terms'])
    return render_template(template, pid=pid, record=record, source= source, terms=terms)
