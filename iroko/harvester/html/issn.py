from flask import Flask
from lxml import etree, ElementInclude, html
import xml.etree.ElementTree as ET
import requests
import json
import binascii
from os import urandom
import time
from random import randint
from iroko.harvester.utils import get_iroko_harvester_agent
from iroko.harvester.base import BaseHarvester
from iroko.sources.models import Issn
from invenio_db import db


class IssnHarvester(BaseHarvester):
    """
    TODO: Document this better!!!
    Harvest all cuban ISSN from issn.org"""

    # TODO: all functions private, except process_pipeline

    def __init__(self, work_dir, load_remote=False):
        self.work_dir = work_dir

        self.cuban_issn_file = self.work_dir + '/issn.cuba.json'
        self.cuban_issn_info_file = self.work_dir + '/issn.info.cuba.json'


    def encode_multipart_formdata(self, fields):

        boundary = binascii.hexlify(urandom(16)).decode('ascii')

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


    def get_issn_count(self, res: requests.Response):

        doc1 = html.fromstring(res.text)
        element = doc1.xpath('.//h2[@class="page-items-count search-results-count"]')
        return int(element[0].text.split()[0])


    def get_info_issn(self, issn: str, sess: requests.Session):

        sess.headers.update(get_iroko_harvester_agent())
        url='https://portal.issn.org/resource/ISSN/'+issn+'?format=json'
        response = sess.get(url)

        # text = response.text.replace('\\n', '')
        # return text.replace('\\"', '"')
        return json.loads(response.text)


    def getissn(self, res: requests.Response):

        doc1 = html.fromstring(res.text)
        result = []
        element = doc1.xpath('.//div[@class="item-result-content-text flex-zero"]//p[1]')
        for v in element:
            result.append(v.text_content().split()[1])
        return result


    def request_advanced_search(self):

        url = 'https://portal.issn.org/advancedsearch'

        sess = requests.Session()

        sess.headers.update(get_iroko_harvester_agent())

        response = sess.get(url)

        doc1 = html.fromstring(response.text)
        variable = ["form_build_id","form_id","honeypot_time"]
        variable_id = "advances-search-issn-final-form"
        dictionary = {}

        for v in variable:
            element = doc1.xpath('.//form[@id="' + variable_id + '"]//input[@name="' + v + '"]')
            dictionary[v]=element[0].value

        print(dictionary)
        sleep_time = randint(3, 9)
        print('sleep {0} seconds'.format(sleep_time))
        time.sleep(sleep_time)

        body = {
            'operator':'SHOULD',
            'selectTitle':'all',
            'opSpeTitle':'0',
            'issnOpt':'all',
            'globalField[fld][0][operator]':'MUST',
            'globalField[fld][0][selector]':'country',
            'globalField[fld][0][countryDiv][countrylist][CUB]':'CUB',
            'op':'Search',
            'form_id':dictionary['form_id'],
            'honeypot_time':dictionary['honeypot_time'],
            'form_build_id':dictionary['form_build_id']
        }

        data, content_type = self.encode_multipart_formdata(body)

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Content-Type': content_type,
            'Cache-Control': 'no-cache',
        }

        resp = sess.post(url, data=data, headers=headers)

        return resp, sess


    def process_pipeline(self):
        """get all cuban issn and its info
        return pair issns(array of all issns), infos(dict with issns info)
        """

        issns = self.get_all_issn()
        infos = self.get_all_issns_info(issns)
        return issns, infos


    def get_all_issn(self):
        """get all cuban ISSNs """

        issns = []
        fres, session = self.request_advanced_search()
        issns = self.getissn(fres)

        session.headers.update(get_iroko_harvester_agent())

        sleep_time = randint(3, 9)
        print('sleep {0} seconds'.format(sleep_time))
        time.sleep(sleep_time)

        page = 2
        size = 100
        count = ( self.get_issn_count(fres) - 10 ) / size

        while page < count:
            resp = session.get(fres.url+'&currentpage={0}&size={1}'.format(page, size))
            issns.extend(self.getissn(resp))

            sleep_time = randint(3, 9)
            print('sleep {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)

            page += 1

        return issns


    def get_cuban_issns_json(self, remoteissns):
        if remoteissns:
            issns = self.get_all_issn()
            with open(self.cuban_issn_file, 'w+',  encoding=('UTF-8')) as file_issn:
                if file_issn:
                    json.dump(issns, file_issn)
        else:
            with open(self.cuban_issn_file, 'r') as file_issn:
                issns = json.load(file_issn)

        return issns


    def get_all_issns_info(self, issns):
        session = requests.Session()

        session.headers.update(get_iroko_harvester_agent())

        result = dict()
        with open(self.cuban_issn_info_file, 'r') as file_issn:
            result = json.load(file_issn)
        for issn in issns:
            try:
                print('try getting {0} info'.format(issn))
                result[issn] = self.get_info_issn(issn, session)
            except Exception as e:
                print('error, getting {0} info, error: {1}'.format(issn, e))
                result[issn] = {"error":str(e)}
                pass
            finally:
                print('ok, saving to file')
                with open(self.cuban_issn_info_file, 'w+',  encoding=('UTF-8')) as file_issn:
                    print('writing to file {0}'.format(self.cuban_issn_info_file))
                    json.dump(result, file_issn)

                sleep_time = randint(4, 7)
                print('finally, sleep {0} seconds'.format(sleep_time))
                time.sleep(sleep_time)
        return result


    def get_cuban_issns_info_json(self, issns, remoteinfo):

        if remoteinfo and issns:
            infos = self.get_all_issns_info(issns)

        else:
            with open(self.cuban_issn_info_file, 'r') as file_issn:
                infos = json.load(file_issn)

        return infos


    def syncronize_files_issn_model(self):
        """
        sincroniza lo que  hay en los ficheros con que trabaja el harvester de issn con el modelo iroko.sources.model.Issn
        """

        with open(self.cuban_issn_file, 'r') as file_issn:
            archive_issn = json.load(file_issn)

        with open(self.cuban_issn_info_file, 'r') as file_issn_info:
            archive_issn_info = json.load(file_issn_info)

        if archive_issn and archive_issn_info:
            for archive in archive_issn:
                issn_model = Issn.query.filter_by(code = archive).first()
                if not issn_model:
                    data = archive_issn_info[archive]
                    obj_issn = Issn()
                    obj_issn.code = archive
                    obj_issn.data = data
                    db.session.add(obj_issn)
                    db.session.flush()
                    db.session.commit()

            return 'success'
        else:
            return 'error'
