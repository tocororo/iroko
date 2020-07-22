

"""Fixtures for users, roles and actions."""

from __future__ import absolute_import, division, print_function

import datetime
import json

from flask import current_app
from invenio_accounts.models import User
from invenio_db import db

import iroko.pidstore.pids as pids
from iroko.harvester.models import HarvestType, Repository
from iroko.sources.api import Sources, IrokoSource
from iroko.sources.models import Source, SourceType, TermSources, SourceStatus, SourceVersion
from iroko.taxonomy.models import Term
from iroko.utils import string_as_identifier


def init_journals():
    # sources_path = '../../data/journals.json'
    delete_all_sources()
    print('delete all source and relations')
    path = current_app.config['INIT_JOURNALS_JSON_PATH']
    path_tax = current_app.config['INIT_TAXONOMY_JSON_PATH']
    path_oai = current_app.config['INIT_OAIURL_JSON_PATH']
    user = User.query.filter_by(email='rafael.martinez@upr.edu.cu').first()

    with open(path) as fsource, open(path_oai) as foai:
        data = json.load(fsource, object_hook=remove_nulls)
        urls = json.load(foai)

        inserted= {}
        if isinstance(data, dict):
            for k, record in data.items():
                if not inserted.__contains__(record['title']):
                    inserted[record['title']] = record['title']
                    print(record['title'])
                    source = dict()
                    source['source_type'] = SourceType.JOURNAL.value
                    source['name'] = record['title']
                    data = dict()
                    ids = []

                    _assing_if_exist(data, record, 'title')
                    _assing_if_exist(data, record, 'description')
                    _assing_if_exist(data, record, 'email')
                    _assing_if_exist(data, record, 'logo')
                    _assing_if_exist(data, record, 'seriadas_cubanas')

                    if 'url' in record:
                        data['url'] = record['url']
                        ids.append(dict(idtype='url', value=record['url']))

                    if 'rnps' in record:
                        data['rnps']= {'p': record['rnps'], 'e': ''}
                        ids.append(dict(idtype='prnps', value=record['rnps']))

                    issn= {}
                    if 'p' in record['issn']:
                        issn['p']=record['issn']['p']
                        ids.append(dict(idtype='pissn', value=record['issn']['p']))
                    if 'e' in record['issn']:
                        issn['e']=record['issn']['e']
                        ids.append(dict(idtype='eissn', value=record['issn']['e']))
                    if 'l' in record['issn']:
                        issn['l']=record['issn']['l']
                        ids.append(dict(idtype='lissn', value=record['issn']['l']))
                    data['issn']= issn

                    for url in urls:
                        if url['id'] == k:
                            data['oaiurl'] = url['url']
                            ids.append(dict(idtype='oaiurl', value=url['url']))

                    data[pids.IDENTIFIERS_FIELD] = ids
                    IrokoSource.delete_pids_without_object(data[pids.IDENTIFIERS_FIELD])

                    source['data']= data
                    msg, new_source = Sources.insert_new_source(source, SourceStatus.UNOFFICIAL, user=user)
                    print(msg)

                    # source.data = data
                    # source.source_status = SourceStatus.UNOFFICIAL
                    # db.session.add(source)
                    # db.session.flush()

    #     db.session.commit()
    init_term_sources()
    # add_terms_to_data()
    # set_initial_versions()
    init_repositories()
    # Sources.sync_source_index()

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

                    # if record.__contains__('source_category'):
                    #     add_term_source(source, record, record['source_category'], tax, 'grupo_mes')

                    # for subid in record["subjects"]:
                    #     add_term_source(source, record, subid, tax, 'subjects')

                    # for ref in record["referecences"]:
                    #     if ref.__contains__('url'):
                    #         add_term_source(source, record, ref['name'], tax, 'data_bases', {'url': ref['url']})
                    #     else:
                    #         add_term_source(source, record, ref['name'], tax, 'data_bases')

        db.session.commit()

def delete_all_sources():
    ts = TermSources.query.all()
    for t in ts:
        db.session.delete(t)
    db.session.commit()
    SourceVersion.query.delete()
    Repository.query.delete()
    # TODO: delete persistentidentifiers and record metadata
    s = Source.query.all()
    for so in s:
        IrokoSource.delete(data={pids.SOURCE_UUID_FIELD: so.uuid})
        IrokoSource.delete_pids_without_object(so.data[pids.IDENTIFIERS_FIELD])
        db.session.delete(so)
    db.session.commit()


def _assing_if_exist(data, record, field):
    if field in record:
        data[field]= record[field]

def get_term_by_name(name):
    term = Term.query.filter_by(name=name).first()
    return term.id

def add_term_source(source, record, tid, tax, tax_key, data=None):

    # tid = record[record_key]
    name = string_as_identifier(tax[tax_key][tid]["name"])
    term = Term.query.filter_by(name=name).first()
    # TODO TermSources deberia trabajar con los UUIDs
    if (term):
        ts = TermSources()
        ts.sources_id = source.id
        ts.term_id = term.id
        ts.data = data
        db.session.add(ts)

def remove_nulls(d):
    return {k: v for k, v in d.items() if v is not None}

def init_repositories():
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
        term_sources = []
        for ts in source.term_sources:
            term_sources.append(
                {
                    'term_id': ts.term_id,
                    'sources_id': source.id,
                    'data': ts.data
                }
            )
        data = dict(source.data)
        data['term_sources'] = term_sources
        source.data = data
    db.session.commit()

def set_initial_versions():

    user = User.query.filter_by(email='rafael.martinez@upr.edu.cu').first()
    sources = Source.query.order_by('name').all()
    for source in sources:
        source_version = SourceVersion()
        source_version.comment = 'initial version'
        source_version.source_id = source.id
        source_version.user_id = user.id
        source_version.data = source.data
        source_version.is_current = True
        source_version.created_at = datetime.date(2019, 1, 1)
        db.session.add(source_version)
        db.session.flush()
    db.session.commit()
