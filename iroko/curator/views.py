
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request, render_template

from flask_login import login_required

from iroko.sources.models import Sources, HarvestType
from iroko.sources.marshmallow import sources_schema, sources_schema_full, source_schema_full


from os import listdir, path

blueprint = Blueprint(
    'iroko_harvester',
    __name__,
    url_prefix='/curator',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/vocabulary/<id>')
@login_required
def edit_vocabulary():
    # the form stuffs...

@blueprint.route('/add/vocabulary')
@login_required
def add_vocabulary():
    # the form stuffs...

@blueprint.route('/term/<id>')
@login_required
def edit_vocabulary():
    # the form stuffs...
