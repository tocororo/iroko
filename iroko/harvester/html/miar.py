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


    def get_url_db(self):
        variable = [
            "http://miar.ub.edu/databases/GRUPO/G",
            "http://miar.ub.edu/databases/GRUPO/S",
            "http://miar.ub.edu/databases/GRUPO/E",
            "http://miar.ub.edu/databases/GRUPO/M"
        ]
        sess = requests.Session()
        sess.headers.update(get_iroko_harvester_agent())
        dictionary = {}

        for url in variable:
            sleep_time = randint(3, 9)
            time.sleep(sleep_time)
            response = sess.get(url)
            doc1 = html.fromstring(response.text)
            element = doc1.xpath('.//span[@id="total_registros"]')
            count_db = element[0].text.split()[0]
            if int(count_db) > 25:
                post_database_miar(url, dictionary, sess, count_db)
            else:
                element_db = doc1.xpath('.//div[@class="table-responsive"]//a')
                for e in element_db:
                    dictionary[e.text] = e.get('href')

        return dictionary

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

    def post_database_miar(self, url:str, dictionary:dict, sess:requests.Session, count):
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
                    dictionary[e.text] = e.get('href')
            else:
                print('ERROR ' + str(resp.status_code) + ' en ' + url)

            value_ini = value_ini +  25

    def get_info_databases(self):
        dictionary = get_url_db()
        dictionary_info = {}
        dictionary_error = {}

        for key, value in dictionary.items():
            try:
                dictionary_info[key] = get_info_db(value)
            except Exception as ex:
                dictionary_error[key] = ex.__str__

            sleep_time = randint(3, 9)
            time.sleep(sleep_time)


        return dictionary_info, dictionary_error

    def get_info_journal(self, issn: str):
        """dado un issn obtener la informacion de esta revista de miar"""

        url = 'http://miar.ub.edu/issn/' + issn

