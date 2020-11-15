from marshmallow import Schema, fields, post_dump, INCLUDE

from iroko.sources.harvesters.issn import IssnDataParser
from iroko.sources.marshmallow.base import SourceDataSchema


# from iroko.harvester.api import SecundarySourceHarvester


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

    # @post_dump
    # def fill_issn_org(self, issn, **kwargs):
    #     for v in ['p','e','l']:
    #         if v in issn:
    #             issn_org = SourceRawData.query.filter_by(identifier = issn[v]).first()
    #             if issn_org:
    #                 data = dict(issn_org.get_data_field('issn'))
    #                 for item in data["@graph"]:
    #                     if item['@id'] == 'resource/ISSN/'+issn[v]+'#KeyTitle':
    #                         issn['issn_org'] = {"issn":issn[v], "title":item["value"]}
    #                         return issn
    #
    #                 #              and issn[v] in issns_with_info.keys():
    #                 # for item in issns_with_info[issn[v]]["@graph"]:
    #                 #     if item['@id'] == 'resource/ISSN/'+issn[v]+'#KeyTitle':
    #                 #         issn['issn_org'] = {"issn":issn[v], "title":item["value"]}
    #                 #         return issn


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

    @post_dump
    def fill_issn_org(self, journal, **kwargs):
        if 'identifiers' not in journal:
            return journal
        issn = ''
        for ids in journal['identifiers']:
            if ids['idtype'] == 'issn_p' or ids['idtype'] == 'issn_e' or ids['idtype'] == 'issn_l':
                issn = ids['value']
                issn_org = IssnDataParser.parse(issn)
                journal['issn_org'] = issn_org
                return journal


# class JournalSchema(BaseSourceSchema):
#     data = fields.Nested(JournalDataSchema, many=False)

journal_data_schema = JournalDataSchema(many=False, unknown=INCLUDE)
# journal_schema = JournalSchema(exclude=['versions'])
# journal_schema_many = JournalSchema(many=True, exclude=['versions'])
