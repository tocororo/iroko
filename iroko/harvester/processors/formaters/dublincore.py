

from iroko.harvester.base import SourceIterator, Formater
from iroko.harvester.processors.oai import nsmap


class DubliCoreElements(Formater):

    def __init__(self, logger):

        self.metadataPrefix ='oai_dc'
        self.logger = logger


    def get_sigle_element(self, metadata, name, language=None):

        # print('get_sigle_element: '+name)
        elements = metadata.findall('.//{' + nsmap['dc'] + '}' + name)
        if len(elements) > 1:
            for e in elements:
                lang='{' + nsmap['xml'] + '}lang'
                if language and lang in e.attrib:
                    if e.attrib[lang] == language:
                        return e.text
            print('self.logger no '+language+' error')
        if len(elements) == 1:
            return elements[0].text
        print('self.logger no name error...')


    def get_multiple_elements(self, metadata, name, itemname=None, language=None):
        # print('get_multiple_elements: '+name)
        results = []
        elements = metadata.findall('.//{' + nsmap['dc'] + '}' + name)
        for e in elements:
            lang='{' + nsmap['xml'] + '}lang'
            if language and lang in e.attrib:
                    if e.attrib[lang] == language:
                        if(itemname == ''):
                            results.append(e.text)
                        else:
                            results.append({itemname: e.text})
            else:
                if(itemname):
                    results.append({itemname: e.text})
                else:
                    results.append(e.text)
        return results


    def ProcessItem(self, xml):
        """given an xml item return a dict, ensure is http://purl.org/dc/elements/1.1/ valid """

        data = {}
        header = xml.find('.//{' + nsmap['oai'] + '}header')
        metadata = xml.find('.//{' + nsmap['oai'] + '}metadata')
        
        identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
        data['original_identifier'] = identifier.text
        identifiers = self.get_multiple_elements(metadata, 'identifier')
        identifiers.insert(0, identifier.text)
        data['identifiers'] = identifiers
        
        data['title'] = self.get_sigle_element(metadata, 'title', 'es-ES')

        creators = self.get_multiple_elements(metadata, 'creator', 'name')
        data['creators'] = creators

        data['keywords'] = self.get_sigle_element(metadata, 'subject', 'es-ES')
        
        data['description'] = self.get_sigle_element(metadata, 'description', 'es-ES')

        data['publisher'] = self.get_sigle_element(metadata, 'publisher', 'es-ES')
        
        data['contributors'] = self.get_sigle_element(metadata, 'contributor', 'es-ES')

        data['publication_date'] = self.get_sigle_element(metadata, 'date', 'es-ES')
        
        types = self.get_multiple_elements(metadata, 'type')
        data['types'] = types

        formats = self.get_multiple_elements(metadata, 'format')
        data['formats'] = formats

        sources = self.get_multiple_elements(metadata, 'source')
        data['sources'] = sources

        data['language'] = self.get_sigle_element(metadata, 'language')

        relations = self.get_multiple_elements(metadata, 'relation')
        #separar el caso especial ref, de lo que realmente significa esto: una url con otro objeto relacionado (asumiendo el caso mas comun: el pdf donde esta el articulo...)
        data['relations'] = relations

        coverages = self.get_multiple_elements(metadata, 'coverage')
        data['coverages'] = coverages

        rights = self.get_multiple_elements(metadata, 'rights')
        data['rights'] = rights
        

        return data
