#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import json
import requests
import bs4 as bs
from lxml import html

website = 'https://wiposearch.ocpi.cu/wopublish-search/public/patents'

patent = {
    "identifiers": "",
    "title": "",
    "authors": [],
    "affiliations": [],
    "country": "",
    "language": "",
    "creation_date": "",
    "grant_date": "",
    "publication_date": "",
    "legal_status": "",
}

def getData(url):
    resultado = requests.get(url)
    content = resultado.text
    soup = bs.BeautifulSoup(content, 'html.parser')
    rows = soup.find('table', {'class': 'table table-view COLUMN'}).find('tbody').find_all('tr')
    for row in rows:
        patent["identifiers"] = row.find_all('td')[2].get_text().rstrip()
        patent["title"] = row.find_all('td')[1].get_text().rstrip()
        patent["authors"] = row.find_all('td')[9].get_text().rstrip()
        patent["affiliations"] = row.find_all('td')[8].get_text().rstrip()
        patent["country"] = "Cuba"
        patent["language"] = "spanish"
        patent["creation_date"] = row.find_all('td')[3].get_text().rstrip()
        patent["grant_date"] = row.find_all('td')[5].get_text().rstrip()
        patent["publication_date"] = row.find_all('td')[6].get_text().rstrip()
        patent["legal_status"] = row.find_all('td')[11].get_text().rstrip()
        json_patent = json.dumps(patent)
        print(json_patent)
    return soup

def nextPage(soup):
    a = soup.find(attrs= {'id': 'id14'})
    url = a['href']
    hfb = url.find(';')
    jh = url.find('?')
    cadena = url[hfb:jh]
    k = url.replace(cadena, '')
    return k

def pagination(url):
    haySiguiente = True
    while(haySiguiente):
        try:
            soup = getData(url)
            url_siguiente = nextPage(soup)
            url = url_siguiente
        except:
            haySiguiente = False

    return 'ok'

print(pagination(website))












