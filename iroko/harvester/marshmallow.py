#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from invenio_records_rest.schemas.fields import DateString
from marshmallow import Schema, fields

from iroko.harvester.models import HarvestType


class RepositorySchema(Schema):
    id = fields.Int(dump_only=True)
    source_id = fields.Int(dump_only=True)
    harvest_type = fields.Str()
    harvest_endpoint = fields.Str()
    last_harvest_run = DateString()
    identifier = fields.Str()
    status = fields.Str()
    error_log = fields.Str()


class GenericRepositorySchema(RepositorySchema):
    formats = fields.Raw()


class OaiRepositoryFormat(Schema):
    setSpec = fields.Str()
    setName = fields.Str()


class OaiRepositorySchema(RepositorySchema):
    formats = fields.Nested(OaiRepositoryFormat, many=True)


class HarvestedItemSchema(Schema):
    id = fields.Int(dump_only=True)
    repository_id = fields.Int()
    identifier = fields.Str()
    record = fields.Str()
    status = fields.Str()
    error_log = fields.Str()


items_schema = HarvestedItemSchema(many=True)


def get_repository_schema(type: HarvestType):
    if type == HarvestType.OAI:
        return OaiRepositorySchema()
    else:
        return GenericRepositorySchema()
