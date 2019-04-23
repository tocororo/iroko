
import requests

from iroko.harvester.processors.oai import OaiIterator
from iroko.harvester.processors.formaters.dublincore import DubliCoreElements


from flask import current_app


path = current_app.config['HARVESTER_FILES_PATH']

def harvest_oai_dc_elements(source):
    formater = DubliCoreElements(None)
    iterator = OaiIterator(None, source, formater)

