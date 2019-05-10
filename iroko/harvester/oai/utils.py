
from iroko.harvester.oai import nsmap


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
