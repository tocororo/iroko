#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from marshmallow import Schema, fields, post_load


class EvaluationSchema(Schema):

    id = fields.Int(dump_only=True)
    uuid = fields.UUID(dump_only=True)
    state = fields.Int(required = False)
    datetime = fields.DateTime(required = True)
    notes = fields.Str(required=False)
    user_id = fields.Int(required = True)

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
        return item


evaluation_schema_many = EvaluationSchema(
    many=True, only=(
        'id', 'uuid', 'state', 'datetime', 'notes', 'user_id')
    )
evaluation_schema = EvaluationSchema(many=False)
