from os import listdir, path
import shutil
from iroko.sources.models import Source
from lxml import etree
from iroko.harvester import utils
from iroko.harvester.oai.formaters import JournalPublishing
from iroko.harvester.oai import nsmap
from iroko.persons.api import IrokoPerson
XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)

harvest_dir = '/Users/malayo/Documents/dev/tocororo/iroko/iroko/data/sceiba-data/100/1/nlm.xml'


xml = etree.parse(harvest_dir, parser=XMLParser)

metadataPrefix ='nlm'
xmlns = '{http://dtd.nlm.nih.gov/publishing/2.3}'
        
        
data = {}
header = xml.find('.//{' + nsmap['oai'] + '}header')
metadata = xml.find('.//{' + nsmap['oai'] + '}metadata')

identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
data['original_identifier'] = identifier.text
setSpec = header.find('.//{' + nsmap['oai'] + '}setSpec')
data['spec'] = setSpec.text

# article_meta = xml.find('.//{' + self.xmlns + '}article-meta')
creators, contributors = IrokoPerson.get_people_from_nlm(metadata)

data['creators'] = creators
data['contributors'] = contributors
print(data)



