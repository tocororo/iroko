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
resultado = requests.get(website)
content = resultado.text

soup = bs.BeautifulSoup(content, 'html.parser')
rows = soup.find('table', {'class': 'table table-view COLUMN'}).find('tbody').find_all('tr')
a = soup.find('table', {'title' : 'Go to next page'})
print(a)
patent = {
    "identifiers": "",
    "title": "",
    "publication_date": "",
    "affiliations": [],
    "authors": [],
    "subtype": "",
    "legal_status": ""
}

for row in rows:
    patent["identifiers"] = str.rstrip(row.find_all('td')[2].get_text())
    patent["title"] = row.find_all('td')[1].get_text().rstrip()
    patent["publication_date"] = row.find_all('td')[6].get_text().rstrip()
    patent["affiliations"] = row.find_all('td')[8].get_text().rstrip()
    patent["authors"] = row.find_all('td')[9].get_text().rstrip()
    patent["subtype"] = row.find_all('td')[10].get_text().rstrip()
    patent["legal_status"] = row.find_all('td')[11].get_text().rstrip()
    json_patents = json.dumps(patent)
    break








