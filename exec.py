from iroko.harvester.models import Repository, RepositorySet, RepositoryStatus, HarvestedItem, HarvestedItemStatus
from iroko.records.api import IrokoRecord


from iroko.sources.models import Sources
from iroko.harvester.models import HarvestedItem
from iroko.harvester.oai.harvester import OaiHarvester
source = Sources.query.filter_by(name='Villena').first()
harvester = OaiHarvester(source)

items = HarvestedItem.query.filter_by(repository_id=harvester.repository.id).all()
for item in items:
    if item.status == HarvestedItemStatus.HARVESTED:
        dc = harvester._process_format(item, harvester.oai_dc)
        nlm = None
        if 'nlm' in harvester.repository.metadata_formats:
            nlm = harvester._process_format(item, harvester.nlm)
        data = harvester._crate_iroko_dict(item, dc, nlm)
        print(data['contributors'])
        # record, status = IrokoRecord.create_or_update(data, dbcommit=True, reindex=True)
        # item.status = HarvestedItemStatus.RECORDED
        # item.record = record.id
# db.session.commit()

# from lxml import etree
# from iroko.harvester.oai.formaters import JournalPublishing

# XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)
# xmlpath = 'data/sceiba-data/53/0/nlm.xml'
# xml = etree.parse(xmlpath, parser=XMLParser)
# formater = JournalPublishing()
# data = formater.ProcessItem(xml)
# print(data)

iterator = harvester.sickle.ListIdentifiers(metadataPrefix=harvester.oai_dc.metadataPrefix)
for item in iterator:
    harvest_item = HarvestedItem.query.filter_by(repository_id=harvester.repository.id,identifier=item.identifier).first()
    harvester._get_all_formats(harvest_item)
    harvest_item.status = HarvestedItemStatus.HARVESTED
db.session.commit()

items = HarvestedItem.query.filter_by(repository_id=harvester.repository.id).all()
for item in items:
    item.status = HarvestedItemStatus.HARVESTED
db.session.commit()





harvester.identity_source()

harvester.discover_items()
harvester.process_items()

# harvester.get_identify()
# harvester.get_formats()
# harvester.get_sets()

# harvester.record_item(item)
item = HarvestedItem.query.filter_by(id=156).first()
dc = harvester._process_format(item, harvester.oai_dc)

from os import path
xmlpath = path.join(harvester.harvest_dir, str(item.id), formater.getMetadataPrefix()+".xml")
# harvester.record_item(item)

# url="http://10.80.3.42/index.php/coodes/oai"

# from iroko.harvester.processors.oai.iterator import OaiIterator
# from iroko.harvester.processors.oai.formaters import DubliCoreElements
# from iroko.harvester.base import Item


# nsmap = {'oai': 'http://www.openarchives.org/OAI/2.0/', 'dc': 'http://purl.org/dc/elements/1.1/', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance','xml':'http://www.w3.org/XML/1998/namespace', 'nlm':'http://dtd.nlm.nih.gov/publishing/2.3'}

# XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)

# idxml = etree.parse("data/harvester/1/0/id.xml", parser=XMLParser)
# # print(idxml)
# # for chi in idxml.getiterator():
# #     print(chi)
# id = idxml.find('.//{' + nsmap['oai'] + '}' + 'identifier')
# print(id.text)

# nlm = etree.parse('data/harvester/0/nlm.xml', parser=XMLParser)
# group = nlm.find('.//{' + nsmap['nlm'] + '}' + 'contrib-group')
# for contrib in group.findall('.//{' + nsmap['nlm'] + '}' + 'contrib'):
#     print(contrib)
#     print(contrib.attrib['contrib-type'])

# nlm_xmlschema = etree.parse('iroko/harvester/schemas/journalpublishing.xsd')
# validator = etree.XMLSchema(nlm_xmlschema)
# if validator.validate(nlm):
#     print('VALID')
# else:
#     print('in-VALID')


# source = {'id':"1", 'havest_endpoint': url}
# formater = DubliCoreElements(None)
# iterator = OaiIterator(None, source,  init_directory=False)
# count=0
# for item in iterator.formats:
#     count+=1
#     print(item)
# print(count)

# iterator.get_identifiers()
# iterator.get_all_metadata()

# iterator.harvest_relation_resources('0')

# from lxml import etree

# from sickle import Sickle
# request = Sickle(url, encoding=None)

# id = 'oai:cfores.upr.edu.cu:article/123'

# arguments ={}
# formats = request.ListMetadataFormats(**arguments)
# for f in formats:
#     print('METADATA FORMATS')
#     print(f.metadataPrefix)
# arguments ={'identifier': id,'metadataPrefix':"oai_dc"}
# record = request.GetRecord(**arguments)
# # print(record)
# # print(record._oai_namespace)



# oai = record.xml
# data = formater.ProcessItem(oai)
# print(data)

# print(etree.tostring(oai))
# oai_xmlschema = etree.parse('./data/schemas/OAI-PMH.xsd')
# oai_validator = etree.XMLSchema(oai_xmlschema)

# oai_validator.assertValid(oai)

# print(metadata)
# oai_dc= metadata.getchildren()[0]
# print(oai_dc)
# nsmap = {'oai': 'http://www.openarchives.org/OAI/2.0/', 'dc': 'http://purl.org/dc/elements/1.1/', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance','xml':'http://www.w3.org/XML/1998/namespace'}

# header = oai.find('.//{' + nsmap['oai'] + '}header')
# metadata = oai.find('.//{' + nsmap['oai'] + '}metadata')

# identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
# print(identifier.text)

# # for e in metadata.xpath('./dc:title',  namespaces=nsmap):
# for e in metadata.findall('.//{' + nsmap['dc'] + '}title'):
#     print('NEW ELEMENT: ')
#     print(e.tag)
#     print(e.text)
#     lang='{' + nsmap['xml'] + '}lang'
#     print(e.attrib[lang])
#     if lang in e.attrib:
#         print(e.attrib[lang])


# # f = open('./data/dc.xsd')
# dc_xmlschema = etree.parse('./data/schemas/oai_dc.xsd')
# validator = etree.XMLSchema(dc_xmlschema)

# oai_dc= metadata.getchildren()[0]
# # print()
# # sss = StringIO()
# # doc = etree.fromstring(etree.tostring(oai_dc))
# # log= validator.error_log

# # validator.assertValid(oai_dc)

# if validator.validate(oai_dc):
#     print('VALID')
# else:
#     print('in-VALID')
#     error = log.last_error
#     print(log)
    
# def parse(oai_record):

#     elem = oai_record.xml.find('.//' + oai_record._oai_namespace + 'metadata')

#     # title_elements = oai_record.xml.findall('.//dc:title', oai_record._oai_namespace)  

#     print(oai_record._oai_namespace)
#     print(elem)
#     # print(title_elements)