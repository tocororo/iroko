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

class MiarHarvester(BaseHarvester):

    def __init__(self, path, load_remote=False):
        self.path = path
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
            with open(self.path, 'r') as file_db:
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
        with open(self.path, 'w') as file_db:
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
                                json.dump(self.miar_groups, file_db)
                        finally:
                            sleep_time = randint(3, 9)
                            print('finally, sleep {0} seconds'.format(sleep_time))
                            time.sleep(sleep_time)


    def get_info_database_recheck(self):
        with open(self.path, 'w') as file_db:
            for group in self.miar_groups:
                for db in group['dbs']:
                    if 'url' in db and 'info' in db and db['info'] == 'ERROR':
                        try:
                            print('getting info of {0}'.format(db['url']))
                            db['info'] = self.get_info_db(db['url'])
                        except Exception as ex:
                            print('ERROR, getting {0}'.format(db['url']))
                            db['info'] = 'ERROR'
                        else:
                            print('ok, saving to file')
                            if file_db:
                                json.dump(self.miar_groups, file_db)
                        finally:
                            sleep_time = randint(3, 9)
                            print('finally, sleep {0} seconds'.format(sleep_time))
                            time.sleep(sleep_time)


    def get_info_journal(self, issn: str):
        """dado un issn obtener la informacion de esta revista de miar,
        da toda la informacion presente en el tab de la revista y los icds anuales"""

        url = 'http://miar.ub.edu/issn/' + issn

