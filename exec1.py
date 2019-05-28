from os import listdir, path
import shutil
from iroko.sources.models import Source
from lxml import etree
from iroko.harvester import utils

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)

harvest_dir = '/Users/malayo/Documents/dev/tocororo/iroko/iroko/data/sceiba-data/123/1.old/id.xml'


xml = etree.parse(harvest_dir, parser=XMLParser)

identifier = xml.find('.//{' + utils.xmlns.oai() + '}identifier')

print(identifier.text)




Traceback (most recent call last):  File "/Users/malayo/Documents/dev/tocororo/iroko/iroko/iroko/harvester/oai/harvester.py", line 293, in record_items    if 'nlm' in self.source.metadata_formats:AttributeError: 'Source' object has no attribute 'metadata_formats'During handling of the above exception, another exception occurred:Traceback (most recent call last):  File "/Users/malayo/Documents/dev/tocororo/iroko/iroko/iroko/harvester/oai/harvester.py", line 109, in process_items    self.record_items()  File "/Users/malayo/Documents/dev/tocororo/iroko/iroko/iroko/harvester/oai/harvester.py", line 301, in record_items    item.error_log += traceback.format_exc()TypeError: unsupported operand type(s) for +=: 'NoneType' and 'str'