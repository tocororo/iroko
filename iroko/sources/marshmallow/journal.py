
from marshmallow import Schema, fields, pre_dump, post_load, post_dump, INCLUDE


from iroko.harvester.api import SecundarySourceHarvester

from iroko.sources.marshmallow.base import SourceDataSchema

class SocialNetworksSchema(Schema):
    facebook = fields.Url()
    twitter = fields.Url()
    linkedin = fields.Url()

class IssnOrgSchema(Schema):
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

class RNPSSchema(Schema):
    p = fields.Str()
    e = fields.Str()


class JournalDataSchema(SourceDataSchema):
    """JournalDataSchema specific data for academic journals """

    url = fields.Url()
    issn = fields.Nested(ISSNSchema, many=False)
    rnps = fields.Nested(RNPSSchema, many=False)
    # TODO add here email = fields.Email(), and TEST....
    email = fields.Str()
    logo = fields.Str()
    seriadas_cubanas = fields.Url()
    start_year = fields.Str()
    end_year = fields.Str()

    subtitle = fields.Str()
    shortname = fields.Str()
    purpose = fields.Str()
    frequency = fields.Str()

    socialNetworks = fields.Nested(SocialNetworksSchema, many=False)

# class JournalSchema(BaseSourceSchema):
#     data = fields.Nested(JournalDataSchema, many=False)

journal_data_schema = JournalDataSchema(many=False, unknown=INCLUDE)
# journal_schema = JournalSchema(exclude=['versions'])
# journal_schema_many = JournalSchema(many=True, exclude=['versions'])
