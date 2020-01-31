

"""Fixtures for users, roles and actions."""

from __future__ import absolute_import, division, print_function

from flask import current_app
import json
import datetime

from invenio_db import db
from invenio_accounts.models import User
from iroko.taxonomy.models import Term
from iroko.sources.models import Source, SourceType, TermSources, SourceStatus, SourceVersion
from iroko.harvester.models import HarvestType, Repository

def init_journals():
    # sources_path = '../../data/journals.json'
    delete_all_sources()
    path = current_app.config['INIT_JOURNALS_JSON_PATH']
    path_tax = current_app.config['INIT_TAXONOMY_JSON_PATH']
    with open(path) as fsource, open(path_tax) as ftax:
        data = json.load(fsource, object_hook=remove_nulls)
        tax = json.load(ftax)
        inserted= {}
        user = User.query.filter_by(email='rafael.martinez@upr.edu.cu').first()
        if isinstance(data, dict):
            for k, record in data.items():
                if not inserted.__contains__(record['title']):
                    inserted[record['title']] = record['title']
                    source = Source()
                    source.source_type = SourceType.JOURNAL
                    source.name = record['title']
                    data = {}
                    _assing_if_exist(data, record, 'title')
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
                    source.source_status = SourceStatus.UNOFFICIAL
                    db.session.add(source)
                    db.session.flush()

                    source_version = SourceVersion()
                    source_version.comment = 'initial version'
                    source_version.source_id = source.id
                    source_version.user_id = user.id
                    source_version.data = data
                    source_version.is_current = True
                    source_version.created_at = datetime.date(2019, 1, 1)
                    db.session.add(source_version)
                    db.session.flush()
        db.session.commit()
    init_term_sources()
    add_terms_to_data()


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
                    source = Source.query.filter_by(name=record['title']).first()

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
    s = Source.query.all()
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
    # TODO TermSources deberia trabajar con los UUIDs
    ts = TermSources()
    ts.sources_id = source.id
    ts.term_id = term.id
    ts.data = data
    db.session.add(ts)


def remove_nulls(d):
    return {k: v for k, v in d.items() if v is not None}

def add_oaiurls():
    path = current_app.config['INIT_JOURNALS_JSON_PATH']
    path_oai = current_app.config['INIT_OAIURL_JSON_PATH']
    with open(path) as fsource, open(path_oai) as foai:
        journals = json.load(fsource, object_hook=remove_nulls)
        urls = json.load(foai)
        if isinstance(journals, dict):
            for k, record in journals.items():
                src = Source.query.filter_by(name=record['title']).first()
                if src:
                    # src.repo_harvest_type = None
                    for url in urls:
                        if url['id'] == k:
                            # print(k)
                            # print(record['id'])
                            print(url['url'])
                            # print(src.data['url'])
                            repo = Repository()
                            repo.harvest_endpoint = url['url']
                            repo.harvest_type = HarvestType.OAI
                            repo.source_id = src.id
                            db.session.add(repo)
                            # src.repo_harvest_endpoint = url['url']
                            # src.repo_harvest_type = HarvestType.OAI
                            # src.repository = repo
            db.session.commit()

def add_terms_to_data():
    sources = Source.query.order_by('name').all()
    for source in sources:
        terms = []
        for ts in source.terms:
            terms.append({'id': ts.term_id, 'data': ts.data})
        data = dict(source.data)
        data['terms'] = terms
        source.data = data
    db.session.commit()
