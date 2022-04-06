#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from marshmallow import INCLUDE, Schema, fields, post_dump
from marshmallow_enum import EnumField
from sqlalchemy import desc

from iroko.harvester.marshmallow import RepositorySchema
from iroko.sources.api import SourceRecord
from iroko.sources.marshmallow.base import (
    SourceDataSchema, TermSourcesSchema, source_base_data_schema,
    )
from iroko.sources.marshmallow.journal import journal_data_schema
from iroko.sources.models import Source, SourceStatus, SourceType, SourceVersion
from iroko.userprofiles import UserProfile
from iroko.userprofiles.marshmallow import UserProfilesSchema, userprofile_schema


class SourceVersionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    source_uuid = fields.Str()
    comment = fields.Str()
    created_at = fields.DateTime()
    is_current = fields.Boolean()
    data = fields.Nested(SourceDataSchema, many=False, unknown=INCLUDE)
    reviewed = fields.Boolean()

    # user = fields.Nested(IrokoUserSchema)

    userprofile = fields.Nested(UserProfilesSchema)

    @post_dump(pass_original=True)
    def fix_data_field(self, result, version: SourceVersion, **kwargs):

        source = SourceRecord.get_record(version.source_uuid)
        # print('************* POST DUMP ***************')
        # print(source.model.json['source_type'], )
        if source.model.json['source_type'] == SourceType.JOURNAL.value:
            data = journal_data_schema.dump(version.data)
        else:
            data = source_base_data_schema.dump(version.data)
        result['data'] = data
        # print('************* POST DUMP ***************')
        return result

    @post_dump(pass_original=True)
    def dump_user_profile(self, result, version: SourceVersion, **kwargs):
        profile = UserProfile.get_or_create_by_userid(version.user_id)
        result['userprofile'] = userprofile_schema.dump(profile)
        return result


class SourceSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    name = fields.Str(allow_none=False)

    source_type = EnumField(SourceType, allow_none=False)
    source_status = EnumField(SourceStatus, allow_none=True)

    term_sources = fields.List(fields.Nested(TermSourcesSchema))
    versions = fields.Nested(SourceVersionSchema, many=True)
    repository = fields.Nested(RepositorySchema)

    data = fields.Nested(SourceDataSchema, many=False, unknown=INCLUDE)

    @post_dump(pass_original=True)
    def fix_data_field(self, result, source: Source, **kwargs):
        # este metodo hace lento el dump, solo es necesario cuando se requiere un source,
        # para una lista, es mejor no hacer el metodo, porque es muy lento.
        if not kwargs['many']:
            if source.source_type == SourceType.JOURNAL:
                # print("is a journal !!!!! #######")
                data = journal_data_schema.dump(source.data)
            else:
                data = source_base_data_schema.dump(source.data)
            result['data'] = data
        return result

    @post_dump
    def dump_need_review_version(self, source, **kwargs):
        # TODO: version_to_review is true cuando tiene una version con una fecha posterior a la
        #  version current.
        versions = SourceVersion.query.filter_by(source_id=source['id']).order_by(
            desc(SourceVersion.created_at)
            ).first()
        if versions and not versions.is_current:
            source['version_to_review'] = True
        else:
            source['version_to_review'] = False

        return source


class IssnSchema(Schema):
    id = fields.Int(dump_only=True)
    identifier = fields.Str(required=True)
    issn_data = fields.Raw(many=False)
    miar_data = fields.Raw(many=False)


source_schema_many = SourceSchema(
    many=True, exclude=['versions', 'term_sources', 'data', 'repository']
    )
source_schema = SourceSchema()
source_schema_no_versions = SourceSchema(exclude=['versions'])

source_version_schema = SourceVersionSchema()
source_version_schema_many = SourceVersionSchema(many=True)
issn_schema = IssnSchema()
