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
from iroko.sources.api import Sources
from iroko.sources.marshmallow import source_schema_full
from iroko.sources.models import Source, HarvestType, SourcesType
from iroko.taxonomy.models import Vocabulary, Term
from flask_babelex import lazy_gettext as _


blueprint = Blueprint(
    'iroko_theme',
    __name__,
    template_folder='templates',
    static_folder='static',
)

@blueprint.route('/')
def index():
    """Simplistic front page view."""
    vocabularies = Vocabulary.query.all()
    vocab_stats = []
    for vocab in vocabularies:
        vocab_stats.append({vocabularies.name:str(Term.query.filter_by(vocabulary_id=vocab.id).count())})  

    return render_template(
        current_app.config['THEME_FRONTPAGE_TEMPLATE'],
        vocabularies=vocabularies,
        vocab_stats=vocab_stats

    )


@blueprint.route('/catalog')
@register_menu(blueprint, 'main.catalog', _('Journal Catalog'), order=2)
def catalogo():

    return render_template('iroko_theme/catalog/index.html', static_host='https://crai-static.upr.edu.cu/', iroko_catalog='https://sceiba-lab.upr.edu.cu/catalog')


@blueprint.route('/source/<uuid>')
def view_source_id(uuid):
    src = Sources.get_source_by_id(uuid=uuid)
    source = source_schema_full.dump(src)
    return render_template('iroko_theme/sources/source.html', source=source.data)


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
