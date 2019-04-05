#only for testing stuffs... 

# url="http://10.80.3.42/index.php/coodes/oai"

url="http://192.168.56.7/index.php/cfores/oai"

from lxml import etree
from sickle import Sickle
request = Sickle(url, encoding=None)

id = 'oai:cfores.upr.edu.cu:article/123'

arguments ={}
formats = request.ListMetadataFormats(**arguments)
for f in formats:
    print('METADATA FORMATS')
    print(f.metadataPrefix)
arguments ={'identifier': id,'metadataPrefix':"oai_dc"}
record = request.GetRecord(**arguments)
# print(record)
# print(record._oai_namespace)
oai = record.xml
# print(etree.tostring(oai))
# oai_xmlschema = etree.parse('./data/schemas/OAI-PMH.xsd')
# oai_validator = etree.XMLSchema(oai_xmlschema)

# oai_validator.assertValid(oai)

# print(metadata)
# oai_dc= metadata.getchildren()[0]
# print(oai_dc)
nsmap = {'oai': 'http://www.openarchives.org/OAI/2.0/', 'dc': 'http://purl.org/dc/elements/1.1/', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance','xml':'http://www.w3.org/XML/1998/namespace'}

header = oai.find('.//{' + nsmap['oai'] + '}header')
metadata = oai.find('.//{' + nsmap['oai'] + '}metadata')

identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
print(identifier.text)

# for e in metadata.xpath('./dc:title',  namespaces=nsmap):
for e in metadata.findall('.//{' + nsmap['dc'] + '}title'):
    print('NEW ELEMENT: ')
    print(e.tag)
    print(e.text)
    lang='{' + nsmap['xml'] + '}lang'
    print(e.attrib[lang])
    if lang in e.attrib:
        print(e.attrib[lang])


# f = open('./data/dc.xsd')
dc_xmlschema = etree.parse('./data/schemas/oai_dc.xsd')
validator = etree.XMLSchema(dc_xmlschema)

oai_dc= metadata.getchildren()[0]
# print()
# sss = StringIO()
# doc = etree.fromstring(etree.tostring(oai_dc))
# log= validator.error_log

# validator.assertValid(oai_dc)

if validator.validate(oai_dc):
    print('VALID')
else:
    print('in-VALID')
    # error = log.last_error
    # print(log)
    
# def parse(oai_record):

#     elem = oai_record.xml.find('.//' + oai_record._oai_namespace + 'metadata')

#     # title_elements = oai_record.xml.findall('.//dc:title', oai_record._oai_namespace)  

#     print(oai_record._oai_namespace)
#     print(elem)
#     # print(title_elements)