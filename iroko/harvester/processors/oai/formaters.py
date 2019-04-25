

from iroko.harvester.base import SourceIterator, Formater
from iroko.harvester.processors.oai import nsmap

from .utils import get_sigle_element, get_multiple_elements

class DubliCoreElements(Formater):

    def __init__(self, logger):

        self.metadataPrefix ='oai_dc'
        self.xmlns = 'http://purl.org/dc/elements/1.1/'


    def ProcessItem(self, xml):
        """given an xml item return a dict, ensure is http://purl.org/dc/elements/1.1/ valid """

        data = {}
        header = xml.find('.//{' + nsmap['oai'] + '}header')
        metadata = xml.find('.//{' + nsmap['oai'] + '}metadata')
        
        identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
        data['original_identifier'] = identifier.text
        identifiers = get_multiple_elements(metadata, 'identifier', xmlns=self.xmlns, itemname=None, language=None)
        identifiers.insert(0, identifier.text)
        data['identifiers'] = identifiers
        
        data['title'] = get_sigle_element(metadata, 'title', xmlns=self.xmlns, language='es-ES')

        creators = get_multiple_elements(metadata, 'creator', xmlns=self.xmlns, itemname='name')
        data['creators'] = creators

        data['keywords'] = get_sigle_element(metadata, 'subject', xmlns=self.xmlns, language='es-ES')
        
        data['description'] = get_sigle_element(metadata, 'description', xmlns=self.xmlns, language='es-ES')

        data['publisher'] = get_sigle_element(metadata, 'publisher', xmlns=self.xmlns, language='es-ES')
        
        data['contributors'] = get_sigle_element(metadata, 'contributor', xmlns=self.xmlns, language='es-ES')

        data['publication_date'] = get_sigle_element(metadata, 'date', xmlns=self.xmlns, language='es-ES')
        
        types = get_multiple_elements(metadata, 'type', xmlns=self.xmlns)
        data['types'] = types

        formats = get_multiple_elements(metadata, 'format', xmlns=self.xmlns)
        data['formats'] = formats

        sources = get_multiple_elements(metadata, 'source', xmlns=self.xmlns)
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

    def __init__(self, logger):

        self.metadataPrefix ='nlm'
        self.xmlns = 'http://dtd.nlm.nih.gov/publishing/2.3'


    def ProcessItem(self, xml):
        """given an xml item return a dict, ensure is http://purl.org/dc/elements/1.1/ valid """

        data = {}
        header = xml.find('.//{' + nsmap['oai'] + '}header')
        metadata = xml.find('.//{' + nsmap['oai'] + '}metadata')
        
        identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
        data['original_identifier'] = identifier.text
        identifiers = get_multiple_elements(metadata, 'identifier', xmlns=self.xmlns, itemname=None, language=None)
        identifiers.insert(0, identifier.text)
        data['identifiers'] = identifiers
        
        data['title'] = get_sigle_element(metadata, 'title', xmlns=self.xmlns, language='es-ES')

        creators = get_multiple_elements(metadata, 'creator', xmlns=self.xmlns, itemname='name')
        data['creators'] = creators

        data['keywords'] = get_sigle_element(metadata, 'subject', xmlns=self.xmlns, language='es-ES')
        
        data['description'] = get_sigle_element(metadata, 'description', xmlns=self.xmlns, language='es-ES')

        data['publisher'] = get_sigle_element(metadata, 'publisher', xmlns=self.xmlns, language='es-ES')
        
        data['contributors'] = get_sigle_element(metadata, 'contributor', xmlns=self.xmlns, language='es-ES')

        data['publication_date'] = get_sigle_element(metadata, 'date', xmlns=self.xmlns, language='es-ES')
        
        types = get_multiple_elements(metadata, 'type', xmlns=self.xmlns)
        data['types'] = types

        formats = get_multiple_elements(metadata, 'format', xmlns=self.xmlns)
        data['formats'] = formats

        sources = get_multiple_elements(metadata, 'source', xmlns=self.xmlns)
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
