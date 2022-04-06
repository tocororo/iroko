#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Fixtures for users, roles and actions."""

from __future__ import absolute_import, division, print_function

import datetime
import json
import os
from time import sleep

from flask import current_app
from invenio_accounts.models import User
from invenio_db import db

import iroko.pidstore.pids as pids
from iroko.harvester.models import HarvestType, Repository
from iroko.sources.api import SourceRecord
from iroko.sources.harvesters.issn import IssnDataParser
from iroko.sources.models import Source, SourceStatus, SourceType, SourceVersion, TermSources
from iroko.utils import CuorHelper, get_default_user, string_as_identifier
from iroko.vocabularies.models import Term


def init_repos():
    datadir = current_app.config['IROKO_DATA_DIRECTORY']

    path = os.path.join(datadir, 'repos.json')
    user = get_default_user()

    with open(path) as repos:
        raw = json.load(repos, object_hook=remove_nulls)
        for k, record in raw.items():
            source = dict()
            data = dict()
            data['source_type'] = SourceType.REPOSITORY.value
            data['name'] = record['name']
            data['title'] = record['name']
            ids = []

            if 'url' in record:
                data['url'] = record['url']
                ids.append(dict(idtype='url', value=record['url']))
            if 'oaiurl' in record:
                data['oaiurl'] = record['oaiurl']
                ids.append(dict(idtype='oaiurl', value=record['oaiurl']))

            data[pids.IDENTIFIERS_FIELD] = ids

            source['data'] = data

            data['source_status'] = SourceStatus.UNOFFICIAL.value

            user = get_default_user()
            data['_save_info'] = {
                'user_id': str(user.id),
                'comment': 'seed data',
                'updated': str(datetime.date.today())
                }

            new_source = SourceRecord.new_source_revision(data, user.id, 'seed data')


def init_journals():
    # sources_path = '../../data/journals.json'
    # delete_all_sources()
    # print('delete all source and relations')
    datadir = current_app.config['IROKO_DATA_DIRECTORY']

    path = os.path.join(datadir, 'journals.json')
    path_tax = os.path.join(datadir, 'vocabularies.json')
    path_oai = os.path.join(datadir, 'oaisources.json')

    user = User.query.filter_by(email='rafael.martinez@upr.edu.cu').first()
    org_cache = dict()
    with open(path) as fsource, open(path_oai) as foai, open(path_tax) as ftax:
        data = json.load(fsource, object_hook=remove_nulls)
        urls = json.load(foai)
        tax = json.load(ftax)
        inserted = {}
        if isinstance(data, dict):
            for k, record in data.items():
                if not inserted.__contains__(record['title']):
                    inserted[record['title']] = record['title']
                    # print(record['title'])
                    source = dict()
                    data = dict()

                    data['source_type'] = SourceType.JOURNAL.value
                    data['name'] = record['title']
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
                        data['rnps'] = {'p': record['rnps'], 'e': ''}
                        ids.append(dict(idtype='prnps', value=record['rnps']))

                    issn = {}
                    issn_org = None
                    if 'p' in record['issn']:
                        issn['p'] = record['issn']['p']
                        issn_org = IssnDataParser.parse(record['issn']['p'])
                        # ids.append(dict(idtype='issn_p', value=record['issn']['p']))
                    if 'e' in record['issn']:
                        issn_org = IssnDataParser.parse(record['issn']['e'])
                        issn['e'] = record['issn']['e']
                    if 'l' in record['issn']:
                        issn_org = IssnDataParser.parse(record['issn']['l'])
                        issn['l'] = record['issn']['l']
                    data['issn'] = issn
                    if issn_org:
                        data['name'] = issn_org['name']
                        data['title'] = issn_org['title']
                        data['aliases'] = issn_org['aliases']
                        ids.extend(issn_org['identifiers'])

                    for url in urls:
                        if url['id'] == k:
                            data['oaiurl'] = url['url']
                            ids.append(dict(idtype='oaiurl', value=url['url']))

                    data[pids.IDENTIFIERS_FIELD] = ids
                    # SourceRecord.delete_all_pids_without_object(data[pids.IDENTIFIERS_FIELD])

                    source['data'] = data

                    if 'licence' in record:
                        data['classifications'] = []
                        name = string_as_identifier(tax['licences'][record['licence']]["name"])
                        term = Term.query.filter_by(identifier=name).first()
                        data['classifications'].append(
                            {
                                'id': str(term.uuid), 'description': term.description,
                                'vocabulary': term.vocabulary_id
                                }
                            )
                    if 'institution' in record:
                        # print(tax['institutions'][record['institution']]["name"])
                        data['organizations'] = []
                        if "orgaid" in tax['institutions'][record['institution']]:
                            orgaid = tax['institutions'][record['institution']]["orgaid"]
                            if orgaid in org_cache:
                                org = org_cache[orgaid]
                            else:
                                org = CuorHelper.query_cuor_by_pid(orgaid)
                                org_cache[orgaid] = org
                        else:
                            name = tax['institutions'][record['institution']]["name"]
                            if name in org_cache:
                                org = org_cache[name]
                            else:
                                org = CuorHelper.query_cuor_by_label(name, country='Cuba')
                                org_cache[name] = org
                        if org:
                            data['organizations'].append(
                                {
                                    'id': org['id'],
                                    'name': org['metadata']['name'],
                                    'role': 'MAIN'
                                    }
                                )
                        parent_id = tax['institutions'][record['institution']]['parents'][0]
                        if parent_id != '0':
                            if "orgaid" in tax['institutions'][parent_id]:
                                orgaid = tax['institutions'][parent_id]["orgaid"]
                                if orgaid in org_cache:
                                    parent_org = org_cache[orgaid]
                                else:
                                    parent_org = CuorHelper.query_cuor_by_pid(orgaid)
                                    org_cache[orgaid] = parent_org
                            else:
                                name = tax['institutions'][parent_id]["name"]
                                if name in org_cache:
                                    parent_org = org_cache[name]
                                else:
                                    parent_org = CuorHelper.query_cuor_by_label(
                                        name, country='Cuba'
                                        )
                                    org_cache[name] = parent_org
                            if parent_org:
                                data['organizations'].append(
                                    {
                                        'id': parent_org['id'],
                                        'name': parent_org['metadata']['name'],
                                        'role': 'COLABORATOR'
                                        }
                                    )

                    data['source_type'] = SourceType.JOURNAL.value
                    data['source_status'] = SourceStatus.UNOFFICIAL.value

                    user = get_default_user()
                    data['_save_info'] = {
                        'user_id': str(user.id),
                        'comment': 'seed data',
                        'updated': str(datetime.date.today())
                        }

                    # TODO: en este caso hace falta hacer patch en vez de update, porque ya issn
                    #  trajo datos...
                    new_source = SourceRecord.new_source_revision(data, user.id, 'seed data')
                    # new_source, msg = SourceRecord.create_or_update(data, None, True, True)
                    # # msg, new_source = Sources.insert_new_source(source,
                    # SourceStatus.UNOFFICIAL, user=user)
                    #
                    # if 'oaiurl' in data:
                    #     repo = Repository.query.filter_by(source_uuid=new_source.id).first()
                    #     if not repo:
                    #         repo = Repository()
                    #         repo.source_uuid = new_source.id
                    #     repo.harvest_endpoint = data['oaiurl']
                    #     repo.harvest_type = HarvestType.OAI
                    #     db.session.add(repo)
                    #
                    # IrokoSourceVersions.new_version(new_source.id, data, user=user,
                    # comment='fixing is_current field', is_current=True)

                    # print('-----------------------')
                    # print(new_source)
                    # print('----------------------- sleep 5 seconds')
                    sleep(5)

                    # source.data = data
                    # source.source_status = SourceStatus.UNOFFICIAL
                    # db.session.add(source)
                    # db.session.flush()

    #     db.session.commit()
    # init_term_sources()
    # add_terms_to_data()
    # set_initial_versions()
    # init_repositories()
    # Sources.sync_source_index()


def init_term_sources():
    path = current_app.config['INIT_JOURNALS_JSON_PATH']
    path_tax = current_app.config['INIT_TAXONOMY_JSON_PATH']
    with open(path) as fsource, open(path_tax) as ftax:
        data = json.load(fsource, object_hook=remove_nulls)
        tax = json.load(ftax)
        inserted = {}
        if isinstance(data, dict):
            for k, record in data.items():
                SourceRecord.get()
                if not inserted.__contains__(record['title']):
                    inserted[record['title']] = record['title']
                    source = Source.query.filter_by(name=record['title']).first()

                    if record.__contains__('institution'):
                        add_term_source(source, record, record['institution'], tax, 'institutions')
                    if record.__contains__('licence'):
                        add_term_source(source, record, record['licence'], tax, 'licences')

                    # if record.__contains__('source_category'):
                    #     add_term_source(source, record, record['source_category'], tax,
                    #     'grupo_mes')

                    # for subid in record["subjects"]:
                    #     add_term_source(source, record, subid, tax, 'subjects')

                    # for ref in record["referecences"]:
                    #     if ref.__contains__('url'):
                    #         add_term_source(source, record, ref['name'], tax, 'data_bases',
                    #         {'url': ref['url']})
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
        SourceRecord.delete(data={pids.SOURCE_UUID_FIELD: so.uuid})
        SourceRecord.delete_all_pids_without_object(so.data[pids.IDENTIFIERS_FIELD])
        db.session.delete(so)
    db.session.commit()


def _assing_if_exist(data, record, field):
    if field in record:
        data[field] = record[field]


def get_term_by_name(name):
    term = Term.query.filter_by(identifier=name).first()
    return term.id


def add_term_source(source, record, tid, tax, tax_key, data=None):
    # tid = record[record_key]
    name = string_as_identifier(tax[tax_key][tid]["name"])
    term = Term.query.filter_by(identifier=name).first()
    # TODO TermSources deberia trabajar con los UUIDs
    if (term and source):
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
                            # # print(k)
                            # # print(record['id'])
                            # print(url['url'])
                            # # print(src.data['url'])
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
