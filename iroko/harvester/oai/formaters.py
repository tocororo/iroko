

from iroko.harvester.base import Formater
from iroko.harvester.oai import nsmap

from .utils import get_sigle_element, get_multiple_elements
from iroko.utils import get_identifier_schema

from lxml import etree

from iroko.persons.api import IrokoPerson
from iroko.records import ContributorRole 

import re

class DubliCoreElements(Formater):

    def __init__(self):

        self.metadataPrefix ='oai_dc'
        self.xmlns = 'http://purl.org/dc/elements/1.1/'


    def ProcessItem(self, xml:etree._Element):
        """given an xml item return a dict, ensure is http://purl.org/dc/elements/1.1/ valid """

        data = {}
        header = xml.find('.//{' + nsmap['oai'] + '}header')
        metadata = xml.find('.//{' + nsmap['oai'] + '}metadata')
        
        identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
        data['original_identifier'] = identifier.text
        setSpec = header.find('.//{' + nsmap['oai'] + '}setSpec')
        data['setSpec'] = setSpec.text

        pids = get_multiple_elements(metadata, 'identifier', xmlns=self.xmlns, itemname=None, language=None)
        identifiers = []
        for pid in pids:
            schema = get_identifier_schema(pid)
            if schema:
                identifiers.append({'idtype': schema,'value': pid})
        # identifiers.insert(0, {'idtype': 'oai','value': identifier.text})
        data['identifiers'] = identifiers
        
        data['title'] = get_sigle_element(metadata, 'title', xmlns=self.xmlns, language='es-ES')

        data['contributors'] = []
        creators = get_multiple_elements(metadata, 'creator', xmlns=self.xmlns, itemname='name')
        for creator in creators:
            if isinstance(creator['name'], str) and  contributor['name'] != '':
                creator['roles'] = []
                creator['roles'].append(ContributorRole.Author.value)
                data['contributors'].append(creator)
        
        contributors = get_multiple_elements(metadata, 'contributor', xmlns=self.xmlns, itemname='name', language='es-ES')
        for contributor in contributors:
            if isinstance(contributor['name'], str) and contributor['name'] != '':
                data['contributors'].append(contributor)

        keywords = get_sigle_element(metadata, 'subject', xmlns=self.xmlns, language='es-ES')
        if keywords and isinstance(keywords, str):
            data['keywords'] = re.split('; |, ', keywords)
        
        desc = get_sigle_element(metadata, 'description', xmlns=self.xmlns, language='es-ES')
        if desc and desc != '':
            data['description'] = desc

        data['publisher'] = get_sigle_element(metadata, 'publisher', xmlns=self.xmlns, language='es-ES')

        data['publication_date'] = get_sigle_element(metadata, 'date', xmlns=self.xmlns, language='es-ES')
        
        types = get_multiple_elements(metadata, 'type', xmlns=self.xmlns)
        data['types'] = types

        formats = get_multiple_elements(metadata, 'format', xmlns=self.xmlns)
        data['formats'] = formats

        sources = get_sigle_element(metadata, 'source', xmlns=self.xmlns, language='es-ES')
        data['sources'] = sources

        data['language'] = get_sigle_element(metadata, 'language', xmlns=self.xmlns)

        relations = get_multiple_elements(metadata, 'relation', xmlns=self.xmlns)
        #separar el caso especial ref, de lo que realmente significa esto: una url con otro objeto relacionado (asumiendo el caso mas comun: el pdf donde esta el articulo...)
        data['relations'] = relations

        coverages = get_multiple_elements(metadata, 'coverage', xmlns=self.xmlns)
        data['coverages'] = coverages

        rights = get_multiple_elements(metadata, 'rights', xmlns=self.xmlns)
        data['rights'] = rights

        return data

class JournalPublishing(Formater):

    def __init__(self):

        self.metadataPrefix ='nlm'
        self.xmlns = '{http://dtd.nlm.nih.gov/publishing/2.3}'


    def ProcessItem(self, xml:etree._Element):
        """given an xml item return a dict, ensure is http://dtd.nlm.nih.gov/publishing/2.3 
        is mainly focussed on contributors and authors"""

        data = {}
        header = xml.find('.//{' + nsmap['oai'] + '}header')
        metadata = xml.find('.//{' + nsmap['oai'] + '}metadata')
        
        identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
        data['original_identifier'] = identifier.text
        setSpec = header.find('.//{' + nsmap['oai'] + '}setSpec')
        data['setSpec'] = setSpec.text

        # article_meta = xml.find('.//{' + self.xmlns + '}article-meta')
        contribs = metadata.findall('.//' + self.xmlns + 'contrib')
        cs = []
        for contrib in contribs:
            cs.append(IrokoPerson.get_person_dict_from_nlm(contrib))
        data['contributors'] = cs
        return data
