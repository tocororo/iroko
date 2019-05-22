# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio error handlers."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, render_template
from flask_menu import register_menu

from iroko.sources.models import Sources
from iroko.sources.marshmallow import source_schema_full


blueprint = Blueprint(
    'iroko_theme_frontpage',
    __name__,
    template_folder='templates',
    static_folder='static',
)

@blueprint.route('/')
def index():
    """Simplistic front page view."""
    return render_template(
        current_app.config['THEME_FRONTPAGE_TEMPLATE'],
    )


@blueprint.route('/catalog')
@register_menu(blueprint, 'main.catalog', 'Catalogo de Revistas', order=2)
def catalogo():

    return render_template('iroko_theme/catalog/index.html', static_host='http://200.14.49.24')

@blueprint.route('/catalog/<id>')
def view_source_id(id):
    src = Sources.query.filter_by(uuid=id).first()
    source = source_schema_full.dump(src)
    return render_template('iroko_theme/catalog/source.html', source=source.data)


def unauthorized(e):
    """Error handler to show a 401.html page in case of a 401 error."""
    return render_template(current_app.config['THEME_401_TEMPLATE']), 401


def insufficient_permissions(e):
    """Error handler to show a 403.html page in case of a 403 error."""
    return render_template(current_app.config['THEME_403_TEMPLATE']), 403


def page_not_found(e):
    """Error handler to show a 404.html page in case of a 404 error."""
    return render_template(current_app.config['THEME_404_TEMPLATE']), 404


def internal_error(e):
    """Error handler to show a 500.html page in case of a 500 error."""
    return render_template(current_app.config['THEME_500_TEMPLATE']), 500
