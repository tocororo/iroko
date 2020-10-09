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
from iroko.sources.models import Issn


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

    # text = response.text.replace('\\n', '')
    # return text.replace('\\"', '"')
    return json.loads(response.text)


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

    doc1 = html.fromstring(response.text)
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


class IssnHarvester(BaseHarvester):
    """
    TODO: Document this better!!!
    Harvest all cuban ISSN from issn.org"""

    # TODO: all functions private, except process_pipeline

    def __init__(self, work_dir, country_code='CUB'):

        self.work_dir = os.path.join(work_dir, 'issn')
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)

        self.country_code = country_code
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
            with open(self.issn_list_file, 'w+', encoding=('UTF-8')) as file_issn:
                if file_issn:
                    print(issn_list)
                    json.dump(issn_list, file_issn, ensure_ascii=False)
        else:
            with open(self.issn_list_file, 'r') as file_issn:
                issn_list = json.load(file_issn)

        return issn_list

    def get_issn_info(self, remote):
        issn_list = self.get_issn_list(remote=False)
        if remote and issn_list:
            issn_info = collect_issn_info(issn_list)
            with open(self.issn_info_file, 'w+', encoding=('UTF-8')) as file_issn:
                if file_issn:
                    json.dump(issn_info, file_issn, ensure_ascii=False)
        else:
            with open(self.issn_info_file, 'r') as file_issn:
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
            issn_model = Issn.query.filter_by(code=issn).first()
            print(issn_model)
            if not issn_model:
                obj_issn = Issn()
                obj_issn.code = issn
                obj_issn.data = data
                db.session.add(obj_issn)
                print('NEW')
            else:
                issn_model.data = data
                print('UPDATED')
            db.session.flush()
        db.session.commit()
        print('DB COMMIT')
        #
        #     return 'success'
        #
        # return 'error'
        # TODO: bascicamente aqui lo que hay que hacer es interpretar lo que hay en el json-ld de issn.org
        # y maperar contra el modelo de Source que tenemos creado, o sea, ver los issn (p, e y l....)

# TODO:
# La importacnion tiene que tener en cuenta los 3 tipos de issn
