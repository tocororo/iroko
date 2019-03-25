# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Fixtures for users, roles and actions."""

from __future__ import absolute_import, division, print_function

from flask import current_app
import json

from invenio_db import db

from ..taxonomy.models import Term
from ..sources.models import Sources, SourcesType, TermSources

def init_journals():
    # sources_path = '../../data/journals.json' 
    delete_all_sources()
    path = current_app.config['INIT_JOURNALS_JSON_PATH']
    path_tax = current_app.config['INIT_TAXONOMY_JSON_PATH']
    with open(path) as fsource, open(path_tax) as ftax:
        data = json.load(fsource, object_hook=remove_nulls)
        tax = json.load(ftax)
        inserted= {}
        if isinstance(data, dict):
            for k, record in data.items():
                if not inserted.__contains__(record['title']):
                    inserted[record['title']] = record['title']
                    source = Sources()
                    source.source_type = SourcesType.JOURNAL
                    source.name = record['title']
                    data = {}
                    _assing_if_exist(data, record, 'description')
                    _assing_if_exist(data, record, 'url')
                    _assing_if_exist(data, record, 'rnps')
                    _assing_if_exist(data, record, 'email')
                    _assing_if_exist(data, record, 'logo')
                    _assing_if_exist(data, record, 'seriadas_cubanas')
                    issn= {}
                    _assing_if_exist(issn, record['issn'], 'p')
                    _assing_if_exist(issn, record['issn'], 'e')
                    _assing_if_exist(issn, record['issn'], 'l')
                    data['issn']= issn
                    source.data = data
                    db.session.add(source)
        db.session.commit()
    init_term_sources()
    

def init_term_sources():
    path = current_app.config['INIT_JOURNALS_JSON_PATH']
    path_tax = current_app.config['INIT_TAXONOMY_JSON_PATH']
    with open(path) as fsource, open(path_tax) as ftax:
        data = json.load(fsource, object_hook=remove_nulls)
        tax = json.load(ftax)
        inserted= {}
        if isinstance(data, dict):
            for k, record in data.items():
                if not inserted.__contains__(record['title']):
                    inserted[record['title']] = record['title']
                    source = Sources.query.filter_by(name=record['title']).first()
                    
                    if record.__contains__('institution'):
                        add_term_source(source, record, record['institution'], tax, 'institutions')
                    if record.__contains__('licence'):
                        add_term_source(source, record, record['licence'], tax, 'licences')
                    if record.__contains__('source_category'):
                        add_term_source(source, record, record['source_category'], tax, 'grupo_mes')

                    for subid in record["subjects"]:
                        add_term_source(source, record, subid, tax, 'subjects')
                    
                    for ref in record["referecences"]:
                        if ref.__contains__('url'):
                            add_term_source(source, record, ref['name'], tax, 'data_bases', {'url': ref['url']})
                        else:
                            add_term_source(source, record, ref['name'], tax, 'data_bases')

        db.session.commit()

def delete_all_sources():
    s = Sources.query.all()
    for so in s:
        db.session.delete(so)

    ts = TermSources.query.all()
    for t in ts:
        db.session.delete(t)

    db.session.commit()

def _assing_if_exist(data, record, field):
    if record.__contains__(field):
        data[field]= record[field]

def get_term_by_name(name):
    term = Term.query.filter_by(name=name).first()
    return term.id

def add_term_source(source, record, tid, tax, tax_key, data=None):

    # tid = record[record_key]
    name = tax[tax_key][tid]["name"]
    term = Term.query.filter_by(name=name).first()
    ts = TermSources()
    ts.sources_id = source.id
    ts.term_id = term.id
    ts.data = data
    db.session.add(ts)

def remove_nulls(d):
    return {k: v for k, v in d.items() if v is not None}   