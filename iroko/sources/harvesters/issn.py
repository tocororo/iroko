#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import binascii
import json
import os
import time
from random import randint

import requests
from flask import current_app
from invenio_db import db
from lxml import html

from iroko.harvester.base import BaseHarvester
from iroko.harvester.utils import get_iroko_harvester_agent
from iroko.sources.api import SourceRecord
from iroko.sources.models import SourceRawData, SourceStatus, SourceType
from iroko.utils import get_default_user


def is_issn(code: str) -> bool:
    """
    return true if code is a valid issn
    :param code:
    :return:
    """
    try:
        # TODO: replace this by a regular expression...
        parts = code.split('-')
        if len(parts[0]) == 4 and len(parts[1]) == 4:
            return True
        return False
    except Exception:
        return False


def encode_multipart_formdata(fields):
    boundary = binascii.hexlify(os.urandom(16)).decode('ascii')

    body = (
        "".join("--%s\r\n"
                "Content-Disposition: form-data; name=\"%s\"\r\n"
                "\r\n"
                "%s\r\n" % (boundary, field, value)
                for field, value in fields.items()) +
        "--%s--\r\n" % boundary
    )

    content_type = "multipart/form-data; boundary=%s" % boundary

    return body, content_type


def get_issn_count(res: requests.Response):
    doc1 = html.fromstring(res.text)
    element = doc1.xpath('.//h2[@class="page-items-count search-results-count"]')
    return int(element[0].text.split()[0])


def get_info_issn(issn: str, sess: requests.Session):
    sess.headers.update(get_iroko_harvester_agent())
    url = 'https://portal.issn.org/resource/ISSN/' + issn + '?format=json'
    response = sess.get(url)

    # text = response.content.decode('UTF-8').replace('\\n', '')
    # return text.replace('\\"', '"')

    # TODO: see if we need to do something if response.status_code != 200:

    return json.loads(response.content.decode('UTF-8'))


def getissn(res: requests.Response):
    doc1 = html.fromstring(res.text)
    result = []
    element = doc1.xpath('.//div[@class="item-result-content-text flex-zero"]//p[1]')
    for v in element:
        result.append(v.text_content().split()[1])
    return result


def request_advanced_search(country_code):
    url = 'https://portal.issn.org/advancedsearch'

    sess = requests.Session()

    sess.headers.update(get_iroko_harvester_agent())

    response = sess.get(url)

    doc1 = html.fromstring(response.content.decode('UTF-8'))
    variable = ["form_build_id", "form_id", "honeypot_time"]
    variable_id = "advances-search-issn-final-form"
    dictionary = {}

    for v in variable:
        element = doc1.xpath('.//form[@id="' + variable_id + '"]//input[@name="' + v + '"]')
        dictionary[v] = element[0].value

    print(dictionary)
    sleep_time = randint(3, 9)
    print('sleep {0} seconds'.format(sleep_time))
    time.sleep(sleep_time)

    body = {
        'operator':                                                           'SHOULD',
        'selectTitle':                                                        'all',
        'opSpeTitle':                                                         '0',
        'issnOpt':                                                            'all',
        'globalField[fld][0][operator]':                                      'MUST',
        'globalField[fld][0][selector]':                                      'country',
        'globalField[fld][0][countryDiv][countrylist][' + country_code + ']': country_code,
        'op':                                                                 'Search',
        'form_id':                                                            dictionary['form_id'],
        'honeypot_time':                                                      dictionary['honeypot_time'],
        'form_build_id':                                                      dictionary['form_build_id']
    }

    data, content_type = encode_multipart_formdata(body)

    headers = {
        'User-Agent':    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Content-Type':  content_type,
        'Cache-Control': 'no-cache',
    }

    resp = sess.post(url, data=data, headers=headers)

    return resp, sess


def collect_issn_list(country_code):
    """get all cuban ISSNs """

    issn_list = []
    fres, session = request_advanced_search(country_code)
    issn_list = getissn(fres)

    session.headers.update(get_iroko_harvester_agent())

    sleep_time = randint(3, 9)
    print('sleep {0} seconds'.format(sleep_time))
    time.sleep(sleep_time)

    page = 2
    size = 100
    count = (get_issn_count(fres) - 10) / size

    while page < count:
        print('getting: {0}'.format(fres.url + '&currentpage={0}&size={1}'.format(page, size)))
        resp = session.get(fres.url + '&currentpage={0}&size={1}'.format(page, size))
        issn_list.extend(getissn(resp))

        sleep_time = randint(3, 9)
        print('sleep {0} seconds'.format(sleep_time))
        time.sleep(sleep_time)

        page += 1

    return issn_list


def collect_issn_info(issn_list):
    session = requests.Session()

    session.headers.update(get_iroko_harvester_agent())

    result = dict()

    for issn in issn_list:
        try:
            print('try getting {0} info'.format(issn))
            result[issn] = get_info_issn(issn, session)
        except Exception as e:
            print('error, getting {0} info, error: {1}'.format(issn, e))
            result[issn] = {"error": str(e)}
            pass
        finally:
            print('ok, saving to file')
            # with open(self.issn_info_file, 'w+', encoding=('UTF-8')) as file_issn:
            #     print('writing to file {0}'.format(self.cuban_issn_info_file))
            #     json.dump(result, file_issn, ensure_ascii=False)

            sleep_time = randint(4, 7)
            print('finally, sleep {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)
    return result


def collect_issn_info_single(issn):
    session = requests.Session()

    session.headers.update(get_iroko_harvester_agent())

    result = dict()

    try:
        print('try getting {0} info'.format(issn))
        result[issn] = get_info_issn(issn, session)
    except Exception as e:
        print('error, getting {0} info, error: {1}'.format(issn, e))
        result[issn] = {"error": str(e)}
        pass
    finally:
        print('ok')
        pass
    return result


class IssnDataParser:
    """
    adhoc class for issn.org data,
    assume in
    source = SourceRawData.query.filter_by(identifier=identifier).first()
    data = source.get_data_field('issn')
    jsonschema-LD format
    """

    @classmethod
    def parse(cls, identifier) -> dict:
        """

        :param identifier: to SourceRawData.query.filter_by(identifier=identifier).first()
        :return:
        [list, str, list]
        1- a list with identifiers, valid for a SourceRecord
        2- the mainTitle
        3- all known aliases

        """
        return cls._parse_data(identifier, parse_relations=True)

    @classmethod
    def _parse_data(cls, identifier, parse_relations=False) -> dict:
        """
        helper func
        :param
        :param parse_relations: if True, will analize 'isFormatOf' and 'otherPhysicalFormat' fields
        :return:
        """

        if not is_issn(identifier):
            return None

        main_title = ''
        identifiers = list()
        aliases = list()

        source = SourceRawData.query.filter_by(identifier=identifier).first()
        if not source:
            return None
            # esto significa que no se recolecto el issn, recolectarlo entonces!!!!
            print('NO SOURCE', identifier)
            issndata = collect_issn_info_single(identifier)
            obj_issn = SourceRawData()
            obj_issn.identifier = identifier
            obj_issn.set_data_field('issn', issndata)
            db.session.add(obj_issn)
            db.session.commit()
            source = SourceRawData.query.filter_by(identifier=identifier).first()

        data = source.get_data_field('issn')

        if '@graph' not in data:
            print('NO DATA', identifier, data)
            return None

        for item in data["@graph"]:

            # ISSN Link (issn_l) is the main issn
            if '@type' in item and item['@type'] == 'http://id.loc.gov/ontologies/bibframe/IssnL':
                cls._append_to_identifier_list(identifiers, {'idtype': 'issn_l', 'value': item['value']})

            if '@id' in item and item['@id'] == 'resource/ISSN/' + identifier:
                cls._append_to_identifier_list(identifiers, cls._get_issn(item))

                if 'mainTitle' in item:
                    main_title = item['mainTitle']
                    pass
                if 'name' in item:
                    name = item['name']
                    if type(name) == list:
                        for n in name:
                            cls._append_to_alias_list(aliases, n)
                    else:
                        cls._append_to_alias_list(aliases, name)
                else:
                    print('no name!!!!', identifier)
                    pass

                # issn relations.
                if parse_relations:
                    try:
                        rel = cls._get_relations(item)
                        if main_title == '' and rel.title != '':
                            main_title = rel.title
                        for _id in rel.identifiers:
                            cls._append_to_identifier_list(identifiers, _id)
                        for a in rel.aliases:
                            cls._append_to_alias_list(aliases, a)
                    except Exception as e:
                        # print(e)
                        pass
        if main_title == '':
            print('no mainTitle', identifier)
            if len(aliases) > 0:
                main_title = aliases[0]
        record = dict()
        record['identifiers'] = identifiers
        record['name'] = main_title
        record['title'] = main_title
        record['aliases'] = aliases

        return record

    @classmethod
    def _append_to_identifier_list(cls, id_list: list, id_item):
        append = True
        for id in id_list:
            if id['idtype'] == id_item['idtype']:
                append = False
        if append:
            id_list.append(id_item)

    @classmethod
    def _append_to_alias_list(cls, alias_list: list, alias_item):
        append = True
        for alias in alias_list:
            if alias == alias_item:
                append = False
        if append:
            alias_list.append(alias_item)

    @classmethod
    def _get_relations(cls, item):
        # TODO: 'isFormatOf' is the same as 'otherPhysicalFormat'?
        relations = None
        if 'isFormatOf' in item:
            relations = item['isFormatOf']
        elif 'otherPhysicalFormat' in item:
            relations = item['otherPhysicalFormat']
        else:
            # print('no relations', item)
            pass
        if type(relations) == str:
            issn_rel = relations.split('/').pop()
            return cls._parse_data(issn_rel)
        if type(relations) == list:
            result_ids = list()
            result_alias = list()
            result_title = ''
            for rel in relations:
                issn_rel = rel.split('/').pop()
                rel = cls._parse_data(issn_rel)
                if result_title == '':
                    result_title = rel.title
                result_ids.extend(rel.identifiers)
                result_alias.extend(rel.aliases)

            record = dict()
            record['identifiers'] = result_ids
            record['title'] = result_title
            record['aliases'] = result_alias

            return record

    @classmethod
    def _get_issn(cls, item):
        # desambiguate all issn types
        if item['format'] == 'vocabularies/medium#Online':
            return {'idtype': 'issn_e', 'value': item['issn']}
        if item['format'] == 'vocabularies/medium#Print':
            return {'idtype': 'issn_p', 'value': item['issn']}
        if item['format'] == 'vocabularies/medium#DigitalCarrier':
            return {'idtype': 'issn_c', 'value': item['issn']}
        if item['format'] == 'vocabularies/medium#Other':
            return {'idtype': 'issn_o', 'value': item['issn']}


class IssnHarvester(BaseHarvester):
    """
    TODO: Document this better!!!
    Harvest all cuban ISSN from issn.org"""

    # TODO: all functions private, except process_pipeline

    def __init__(self, work_dir, country_code='CUB', country_id='http://id.loc.gov/vocabulary/countries/cu'):

        self.work_dir = os.path.join(work_dir, 'issn')
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)

        self.country_code = country_code
        self.country_id = country_id

        self.issn_list_file = os.path.join(self.work_dir, self.country_code + '.list.json')
        self.issn_info_file = os.path.join(self.work_dir, self.country_code + '.info.json')

    def process_pipeline(self):
        """get all cuban issn and its info
        return pair issns(array of all issns), infos(dict with issns info)
        """

        issn_list = self.get_issn_list(remote=True)
        issn_info = self.get_issn_info(remote=True)
        return issn_list, issn_info

    def get_issn_list(self, remote):
        if remote:
            issn_list = collect_issn_list(self.country_code)
            with open(self.issn_list_file, 'w+', encoding='UTF-8') as file_issn:
                if file_issn:
                    print(issn_list)
                    json.dump(issn_list, file_issn, ensure_ascii=False)
        else:
            with open(self.issn_list_file, 'r', encoding='UTF-8') as file_issn:
                issn_list = json.load(file_issn)

        return issn_list

    def get_issn_info(self, remote):
        issn_list = self.get_issn_list(remote=False)
        if remote and issn_list:
            issn_info = collect_issn_info(issn_list)
            with open(self.issn_info_file, 'w+', encoding='UTF-8') as file_issn:
                if file_issn:
                    json.dump(issn_info, file_issn, ensure_ascii=False)
        else:
            with open(self.issn_info_file, 'r', encoding='UTF-8') as file_issn:
                issn_info = json.load(file_issn)

        return issn_info


class IssnHarvesterManager:
    @classmethod
    def collect_issn(cls):
        work_dir = current_app.config['IROKO_DATA_DIRECTORY']
        harvester = IssnHarvester(work_dir)

        return harvester.process_pipeline()

        # issns = harvester.get_issn_list(remoteissns)
        #
        # if info:
        #     infos = harvester.get_cuban_issns_info_json(issns, remoteinfo)
        #     # con lo que hay en el dic, crear/actualizar, versiones de source cuyo comentario sea issn...

    # @classmethod
    # def get_cuban_issns(cls):
    #     work_dir = current_app.config['IROKO_DATA_DIRECTORY']
    #     harvester = IssnHarvester(work_dir)
    #
    #     issns = harvester.get_issn_list(False)
    #     infos = harvester.get_cuban_issns_info_json(issns, False)
    #
    #     return infos

    @classmethod
    def sync_db(cls):
        work_dir = current_app.config['IROKO_DATA_DIRECTORY']
        harvester = IssnHarvester(work_dir)
        issn_list = harvester.get_issn_list(remote=False)
        issn_info = harvester.get_issn_info(remote=False)

        for issn in issn_list:
            data = issn_info[issn]
            issn_model = SourceRawData.query.filter_by(identifier=issn).first()
            print(issn_model)
            if not issn_model:
                obj_issn = SourceRawData()
                obj_issn.identifier = issn
                obj_issn.set_data_field('issn', data)
                db.session.add(obj_issn)
                print('NEW')
            else:
                issn_model.set_data_field('issn', data)
                print('UPDATED')
            db.session.flush()
        db.session.commit()
        print('DB COMMIT')

    @classmethod
    def sync_records(cls):

        issn_list = SourceRawData.query.all()
        for issn in issn_list:
            record = IssnDataParser.parse(issn.identifier)
            if record:
                user = get_default_user()
                record['source_status'] = SourceStatus.UNOFFICIAL.value
                record['source_type'] = SourceType.JOURNAL.value
                print(record)
                SourceRecord.new_source_revision(record, user_id=user.id, comment='issn.org import')
                # SourceRecord.create_or_update(record.dump(record))
