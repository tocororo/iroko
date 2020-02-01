from flask import Flask
from lxml import etree, ElementInclude, html
import requests
import xml.etree.ElementTree as ET
import json
import binascii
from os import urandom
import time
from random import randint
from iroko.harvester.utils import get_iroko_harvester_agent
from iroko.harvester.base import BaseHarvester
from iroko.taxonomy.models import Vocabulary, Term, TermClasification
from invenio_db import db


class MiarHarvester(BaseHarvester):

    def __init__(self, work_dir, load_remote=False):
        self.work_dir = work_dir
        self.miar_dbs_file = self.work_dir + '/miar.dbs.json'
        self.miar_journals_file = self.work_dir + '/miar.journals.json'
        self.miar_types_vocab_name = 'miar_types'
        self.miar_database_vocab_name = 'miar_databases'
        if load_remote:
            self.miar_groups = [
                    {
                        'name' : 'WoS / Scopus',
                        'url' : 'http://miar.ub.edu/databases/GRUPO/G'
                    },
                    {
                        'name' : 'Bases de datos multidisciplinares',
                        'url' : 'http://miar.ub.edu/databases/GRUPO/S'
                    },
                    {
                        'name' : 'Bases de datos especializadas',
                        'url' : 'http://miar.ub.edu/databases/GRUPO/E'
                    },
                    {
                    'name' : 'Sistemas de evaluación',
                    'url' : 'http://miar.ub.edu/databases/GRUPO/M'
                    }
                ]
            self.get_url_db()
            self.get_info_databases()
        else:
            with open(self.miar_dbs_file, 'r') as file_db:
                self.miar_groups = json.load(file_db)


    def get_url_db(self):
        sess = requests.Session()
        sess.headers.update(get_iroko_harvester_agent())
        for group in self.miar_groups:
            print('getting group {0}'.format(group['name']))
            group['dbs'] = self.get_db_group(sess, group['url'])


    def get_db_group(self, sess, url):
        result = []

        sleep_time = randint(3, 9)
        time.sleep(sleep_time)
        response = sess.get(url)
        doc1 = html.fromstring(response.text)
        element = doc1.xpath('.//span[@id="total_registros"]')
        count_db = element[0].text.split()[0]
        if int(count_db) > 25:
            self.post_database_miar(url, result, sess, count_db)
        else:
            element_db = doc1.xpath('.//div[@class="table-responsive"]//a')
            for e in element_db:
                result.append({'name':e.text, 'url': e.get('href')})

        return result


    def post_database_miar(self, url:str, result, sess:requests.Session, count):
        value_ini = 0
        value_content_length = 35
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "en-US,en;q=0.5",
            'Connection': "keep-alive",
            'Content-Length': str(value_content_length),
            'Content-Type': "application/x-www-form-urlencoded",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
            'Cache-Control': "max-age=0",
        }

        while  int(count) >= int(value_ini):
            if value_ini > 0:
                value_content_length = 36
            payload = 'directorio=miar&letra=&ini='+str(value_ini)+'&rgs=25'
            headers['Content-Length'] = str(value_content_length)
            sleep_time = randint(3, 9)
            time.sleep(sleep_time)
            resp = sess.post(url, data=payload, headers=headers)

            if resp.status_code == 200:
                doc1 = html.fromstring(resp.text)
                element_db = doc1.xpath('.//div[@class="table-responsive"]//a')
                for e in element_db:
                    result.append({'name':e.text, 'url': e.get('href')})
            else:
                print('ERROR ' + str(resp.status_code) + ' en ' + url)

            value_ini = value_ini +  25


    def get_info_db(self, url):

        sess = requests.Session()
        sess.headers.update(get_iroko_harvester_agent())
        timeout = 30
        dictionary = {}
        response = sess.get(url,timeout = timeout)
        doc1 = html.fromstring(response.text)
        element = doc1.xpath('.//div[@id="gtb_div_base"]//div[@style="display:table-row-group"]')

        for e in element:
            element1 = e.xpath('.//div//div')
            if(element1[1].xpath('.//a')):
                a = element1[1].xpath('.//a')
                dictionary[element1[0].text_content()] = a[0].get('href')
            else:
                dictionary[element1[0].text_content()] = element1[1].text_content().split(sep='\n')[1]
            # sleep_time = randint(3, 9)
            # time.sleep(sleep_time)

        return dictionary


    def get_info_databases(self):
        with open(self.miar_dbs_file, 'w') as file_db:
            for group in self.miar_groups:
                for db in group['dbs']:
                    if 'url' in db:
                        try:
                            print('getting info of {0}'.format(db['url']))
                            db['info'] = self.get_info_db(db['url'])
                        except Exception as ex:
                            print('ERROR, getting {0}'.format(db['url']))
                            db['info'] = 'ERROR'
                        else:
                            print('ok, saving to file')
                            if file_db:
                                file_db.seek(0)
                                json.dump(self.miar_groups, file_db)
                        finally:
                            sleep_time = randint(3, 9)
                            print('finally, sleep {0} seconds'.format(sleep_time))
                            time.sleep(sleep_time)


    def get_info_database_recheck(self):
        print(self.miar_groups)
        for group in self.miar_groups:
            for db in group['dbs']:
                if 'url' in db and (
                    (not 'info' in db) or ('info' in db and db['info'] == 'ERROR')
                ):
                    try:
                        print('getting info of {0}'.format(db['url']))
                        db['info'] = self.get_info_db(db['url'])
                    except Exception as ex:
                        print('ERROR, getting {0}'.format(db['url']))
                        db['info'] = 'ERROR'
                    # else:
                    #     print('ok, saving to file')
                    #     if file_db:
                    #         # This is an error
                    #         file_db.seek(0)

                    finally:
                        sleep_time = randint(3, 9)
                        print('finally, sleep {0} seconds'.format(sleep_time))
                        time.sleep(sleep_time)
        with open(self.miar_dbs_file, 'w+',  encoding=('UTF-8')) as file_db:
            print('writing to file {0}'.format(self.miar_dbs_file))
            json.dump(self.miar_groups, file_db)

    def update_databases_iroko(self):
        # TODO: sincroniza lo que  hay en self.miar_dbs_file con la base de datos de iroko
        with open(self.miar_dbs_file, 'r') as file_dbs:
            archive = json.load(file_dbs)

        miar_db_type_vocab = Vocabulary.query.filter_by(name = 'miar_types').first()
        miar_db_vocab = Vocabulary.query.filter_by(name = 'miar_databases').first()

        if(archive):
            for archive_dbs in archive:
                miar_types = Term()
                miar_types.name = archive_dbs['name']
                miar_types.vocabulary_id = miar_db_type_vocab.id
                miar_types.description = archive_dbs['url']
                db.session.add(miar_types)
                db.session.flush()
                for archive_dbs_info in archive_dbs['dbs']:
                    miar_dbs = Term()
                    miar_dbs.name = archive_dbs_info['name']
                    miar_dbs.vocabulary_id = miar_db_vocab.id
                    miar_dbs.description = archive_dbs_info['url']
                    miar_dbs.data = archive_dbs_info['info']
                    db.session.add(miar_dbs)
                    db.session.flush()
                    miar_classification = TermClasification()
                    miar_classification.term_class_id = miar_types.id
                    miar_classification.term_clasified_id = miar_dbs.id
                    db.session.add(miar_classification)
                    db.session.commit()

            return 'success'
        else:
            return 'error'


    def get_info_from_journals(self, issn_path):
        # TODO: dado la lista de issns en un archivo llamar a get_info_journal y guargar todo en el fichero
        # self.miar_journals_file
        dbs = open(self.miar_dbs_file, 'w')
        print(dbs)
        pass

    def update_journals_iroko(self):
        # TODO: sincroniza lo que  hay en self.miar_journals_file con la base de datos de iroko, es decir,
        pass

    def get_info_journal(self, issn: str):

        url = 'http://miar.ub.edu/issn/' + issn
        sess = requests.Session()
        sess.headers.update(get_iroko_harvester_agent())
        timeout = 30
        dictionary = {}
        response = sess.get(url,timeout = timeout)
        doc1 = html.fromstring(response.text)
        element_not_found = doc1.xpath('.//div[@class="alert alert-danger"]')
        element = doc1.xpath('.//div[@id="gtb_div_Revista"]//div[@style="display:table-row-group"]')
        element_history = doc1.xpath('.//div[@id="mod_versiones"]//a')

        if len(element_not_found) > 0:
            return element_not_found[0].text

        #Info ISSN in actual year
        for e in element:
            element1 = e.xpath('.//div//div')
            if(element1[1].xpath('.//a')):
                a = element1[1].xpath('.//a')
                dictionary[element1[0].text_content()] = a[0].text
            else:
                dictionary[element1[0].text_content()] = element1[1].text_content().split(sep='\n')[1]

        #Info ISSN in past years
        for e_h in element_history:
            element_history1 = e_h.xpath('.//img/@alt')
            url_history = e_h.get('href')
            icds_year = element_history1[0]
            self.get_info_icds(url_history, dictionary, sess, icds_year)
            sleep_time = randint(3, 9)
            time.sleep(sleep_time)

        return dictionary

    def get_info_icds(self, url: str, dictionary:dict, sess:requests.Session, icds_year: str):

        timeout = 30
        response = sess.get(url,timeout = timeout)
        doc1 = html.fromstring(response.text)
        element = doc1.xpath('.//div[@id="sp_icds"]')
        if len(element) > 0:
            dictionary[str(icds_year)] = element[0].text
