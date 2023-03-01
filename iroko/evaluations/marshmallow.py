#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from marshmallow import Schema, fields, post_load
from enum import Enum
from marshmallow_enum import EnumField
from iroko.evaluations.models import EvaluationState


class EvaluationSchema(Schema):

    id = fields.Int()
    uuid = fields.UUID()
    state = EnumField(EvaluationState)
    datetime = fields.DateTime()
    notes = fields.Str(required=False, allow_none=True)
    user_id = fields.Int(required = True)

    entity_name = fields.Str()
    entity_type = fields.Str()
    entity_id_type = fields.Str()
    entity_id_value = fields.Str()

    methodology_schema = fields.Str()
    methodology_name = fields.Str()

    # id = fields.Int(dump_only=True)
    # classification = fields.Str(required=True)
    # description = fields.Str(allow_none=True)
    # receiver_id = fields.Int(required=True)
    # emiter = fields.Str(required=True)
    # viewed = fields.Bool(required=False)

    # in case to put anything in the future
    data = fields.Raw(allow_none=True)

    @post_load
    def evaluation_load(self, item, **kwargs):
        # TODO: Add here fix to the name (no spaces, not capitals... etc...)
        item['state'] = item['state'] if 'state' in item else ''
        item['datetime'] = item['datetime'] if 'datetime' in item else ''
        item['notes'] = item['notes'] if 'notes' in item else ''
        item['user_id'] = item['user_id'] if 'user_id' in item else ''
        item['data'] = item['data'] if 'data' in item else {}
        item['entity_name'] = item['entity_name'] if 'entity_name' in item else ''
        item['entity_type'] = item['entity_type'] if 'entity_type' in item else ''
        item['entity_id_type'] = item['entity_id_type'] if 'entity_id_type' in item else ''
        item['entity_id_value'] = item['entity_id_value'] if 'entity_id_value' in item else ''
        item['methodology_schema'] = item['methodology_schema'] if 'methodology_schema' in item else ''
        item['methodology_name'] = item['methodology_name'] if 'methodology_name' in item else ''
        return item


evaluation_schema_many = EvaluationSchema(
    many=True, only=(
        'id', 'uuid', 'state', 'datetime', 'notes', 'user_id', 'entity_name', 'entity_type', 'methodology_name')
    )
evaluation_schema = EvaluationSchema(many=False)
