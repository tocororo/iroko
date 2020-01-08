# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio error handlers."""

from __future__ import absolute_import, print_function

import os

from flask import Blueprint, current_app, render_template, url_for, redirect, send_from_directory,send_file
from flask_menu import register_menu
from iroko.sources.api import Sources
from iroko.sources.marshmallow import source_schema_full
from iroko.sources.models import Source, HarvestType, SourceType
from iroko.taxonomy.models import Vocabulary, Term
from iroko.harvester.models import HarvestedItem, HarvestedItemStatus
from iroko.deployment import INIT_STATIC_JSON_PATH
from invenio_i18n.selectors import get_locale
from flask_babelex import lazy_gettext as _
from iroko.records.api import IrokoAggs
import json
import mistune
# from invenio_userprofiles.config import USERPROFILES_EXTEND_SECURITY_FORMS


blueprint = Blueprint(
    'iroko_theme',
    __name__,
    template_folder='templates',
    static_folder='static',
)

@blueprint.context_processor
def get_about():
    about = {}
    # with open(current_app.config['INIT_STATIC_JSON_PATH']+'/'+get_locale()+'/texts.json') as file:
    #     texts = json.load(file)
    #     if texts and 'about' in texts.keys():
    #         about = dict(about=texts['about'])
    return about


def get_record_count():
    cant_records = HarvestedItem.query.filter_by(status=HarvestedItemStatus.RECORDED).count()
    return cant_records


@blueprint.route('/')
def index():
    # print(USERPROFILES_EXTEND_SECURITY_FORMS)
    """Simplistic front page view."""
    vocabularies = Vocabulary.query.all()
    vocab_stats = []
    vocab_stats.append({'records':str(get_record_count())})

    sources = IrokoAggs.getAggrs("source.name", 50000)
    vocab_stats.append({'sources':str(len(sources))})

    authors = IrokoAggs.getAggrs("creators.name",50000)
    #print('authors'+str(authors))
    vocab_stats.append({'authors':str(len(authors))})

    # TODO: cuando se vaya a escribir el json es agregarle la opcion w y
    # ensure_ascii=False para que las tildes y demas se pongan bien

    # texts = {}
    # with open(current_app.config['INIT_STATIC_JSON_PATH']+'/'+get_locale()+'/texts.json') as file:
    #     texts = json.load(file)

    texts = ''
    with open(INIT_STATIC_JSON_PATH+'/'+get_locale()+'/faqs.md', 'r') as file:
         texts = file.read()
         file.close()
    markdown = mistune.Markdown()
    faqs = markdown(texts)

    keywords = IrokoAggs.getAggrs("keywords",50000)
    #print('keywords'+str(keywords))
    vocab_stats.append({'Keywords':str(len(keywords))})

    for vocab in vocabularies:
        vocab_stats.append({vocab.name:str(Term.query.filter_by(vocabulary_id=vocab.id).count())})

    return render_template(
        current_app.config['THEME_FRONTPAGE_TEMPLATE'],
        vocabularies=vocabularies,
        vocab_stats=vocab_stats,
        faqs=''
    )


@blueprint.route('/catalog')
@register_menu(blueprint, 'main.catalog', _('Journal Catalog'), order=2)
def catalogo():
    return render_template('iroko_theme/catalog/index.html', iroko_host=current_app.config['IROKO_HOST'])



@blueprint.route('/faq')
@register_menu(blueprint, 'main.faq', _('FAQ'), order=3)
def faq():
    return redirect('/page/faq')


# @blueprint.route('/about')
# @register_menu(blueprint, 'main.about', _('About'), order=4)
# def about():
#     return redirect('/#about')


@blueprint.route('/source/<uuid>')
def view_source_id(uuid):
    src = Sources.get_source_by_id(uuid=uuid)
    source = source_schema_full.dump(src)
    return render_template('iroko_theme/sources/source.html', source=source.data)

@blueprint.route('/aggr/sources')
def view_aggr_sources():
    sources = IrokoAggs.getAggrs("source.name")
    return render_template('iroko_theme/records/aggr.html',name="Sources" ,aggrs=sources,keyword='sources')

@blueprint.route('/aggr/keywords')
def view_aggr_keywords():
    sources = IrokoAggs.getAggrs("keywords")
    return render_template('iroko_theme/records/aggr.html',name="Keywords" ,aggrs=sources,keyword='keywords')

@blueprint.route('/aggr/authors')
def view_aggr_authors():
    sources = IrokoAggs.getAggrs("creators.name")
    return render_template('iroko_theme/records/aggr.html',name="Creators" ,aggrs=sources,keyword='creators')


@blueprint.route('/page/<slug>')
def static_page(slug):
    # 1- load static_pages.json
    # 2- search the slug
    # 3- render appropiate md file (including language....)

    slugs = {}
    aux_text = ''
    with open(INIT_STATIC_JSON_PATH+ '/static_pages.json') as file:
        slugs = json.load(file)
    if slugs:
        with open(INIT_STATIC_JSON_PATH+'/'+get_locale()+'/'+slugs[slug][get_locale()]["url"], 'r') as file:
            aux_text = file.read()
            file.close()
        markdown = mistune.Markdown()
        aux_text = markdown(aux_text)
    return render_template('iroko_theme/static_pages.html', title=slugs[slug][get_locale()]["title"], text=aux_text)

@blueprint.route('/page/images/<image>')
def static_page_image(image):
    directory = os.path.join(INIT_STATIC_JSON_PATH,'images')
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(directory)
    print(image)
    return send_file(os.path.join(directory, image))
    # return send_from_directory(directory, image)

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
