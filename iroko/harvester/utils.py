
from iroko.harvester.oai import nsmap
from collections import defaultdict
import enum
import re

class xmlns():

    @staticmethod
    def oai():
        return 'http://www.openarchives.org/OAI/2.0/'
    @staticmethod
    def oai_identifier():
        return 'http://www.openarchives.org/OAI/2.0/oai-identifier'
    @staticmethod
    def dc():
        return 'http://purl.org/dc/elements/1.1/'
    @staticmethod
    def xsi():
        return 'http://www.w3.org/2001/XMLSchema-instance'
    @staticmethod
    def xml():
        return 'http://www.w3.org/XML/1998/namespace'
    @staticmethod
    def nlm():
        return 'http://dtd.nlm.nih.gov/publishing/2.3'


def get_sigle_element(metadata, name, xmlns='dc', language=None):

    # print('get_sigle_element: '+name)
    elements = metadata.findall('.//{' + xmlns + '}' + name)
    if len(elements) > 1:
        for e in elements:
            lang='{' + nsmap['xml'] + '}lang'
            if language and lang in e.attrib:
                if e.attrib[lang] == language:
                    return e.text
        print('self.logger no '+language+' error')
    if len(elements) == 1:
        return elements[0].text
    # print('self.logger no name error...')


def get_multiple_elements(metadata, name, xmlns='dc', itemname=None, language=None):
    # print('get_multiple_elements: '+name)
    results = []
    elements = metadata.findall('.//{' + xmlns + '}' + name)
    for e in elements:
        lang='{' + nsmap['xml'] + '}lang'
        apend = None
        if language and lang in e.attrib:
                if e.attrib[lang] == language:
                    if(itemname == ''):
                        apend = e.text
                    else:
                        apend = {itemname: e.text}
        else:
            if(itemname):
                apend = {itemname: e.text}
            else:
                apend = e.text
        if e.text is not None and e.text != '' and apend is not None:
            results.append(apend)
    return results

def xml_to_dict(tree, paths=None, nsmap=None, strip_ns=False):
    """Convert an XML tree to a dictionary.

    :param tree: etree Element
    :type tree: :class:`lxml.etree._Element`
    :param paths: An optional list of XPath expressions applied on the XML tree.
    :type paths: list[basestring]
    :param nsmap: An optional prefix-namespace mapping for conciser spec of paths.
    :type nsmap: dict
    :param strip_ns: Flag for whether to remove the namespaces from the tags.
    :type strip_ns: bool
    """
    paths = paths or ['.//']
    nsmap = nsmap or {}
    fields = defaultdict(list)
    for path in paths:
        elements = tree.findall(path, nsmap)
        for element in elements:
            tag = re.sub(
                r'\{.*\}', '', element.tag) if strip_ns else element.tag
            fields[tag].append(element.text)
    return dict(fields)


def get_iroko_harvester_agent():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'}
