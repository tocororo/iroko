
from marshmallow import Schema, fields, pre_dump, post_load, post_dump

from iroko.sources.marshmallow import BaseSourceSchema, SourceDataSchema
from iroko.harvester.api import SecundarySourceHarvester


class IssnOrgSchema:
    issn = fields.Str()
    title = fields.Str()

class ISSNSchema(Schema):
    p = fields.Str()
    e = fields.Str()
    l = fields.Str()

    issn_org = fields.Nested(IssnOrgSchema, many=False)
    # TODO: Comprobar con pre_load que cada campo es un issn valido

    @post_dump
    def fill_issn_org(self, issn, **kwargs):
        # TODO: replace this by database query !!!
        issns_with_info = SecundarySourceHarvester.get_cuban_issns()
        for v in ['p','e','l']:
            if v in issn and issn[v] in issns_with_info.keys():
                    for item in issns_with_info[issn[v]]["@graph"]:
                        if item['@id'] == 'resource/ISSN/'+issn[v]+'#KeyTitle':
                            issn['issn_org'] = {"issn":issn[v], "title":item["value"]}
                            return issn



class JournalDataSchema(SourceDataSchema):
    """JournalDataSchema specific data for academic journals """

    url = fields.Url()
    issn = fields.Nested(ISSNSchema, many=False)
    rnps = fields.Str()
    # TODO add here email = fields.Email(), and TEST....
    email = fields.Str()
    logo = fields.Str()
    seriadas_cubanas = fields.Url()
    year_start = fields.DateTime()
    year_end = fields.DateTime()



class JournalSchema(BaseSourceSchema):
    data = fields.Nested(JournalDataSchema, many=False)

journal_schema = JournalSchema()
journal_schema_many = JournalSchema(many=True)
