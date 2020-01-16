                                                                                                                                        
from marshmallow import Schema, fields, ValidationError, pre_load, pre_dump, post_load, post_dump
from iroko.notifications.models import Notification


class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    receiver = fields.Int(required=True)
    emiter = fields.Str(required=True)
    viewed = fields.Bool(required=True)
    
    # in case to put anything in the future
    data = fields.Raw(allow_none=True)

    @post_load
    def notification_load(self, item, **kwargs):
        # TODO: Add here fix to the name (no spaces, not capitals... etc...)
        item['description'] = item['description'] if 'description' in item else ''
        item['data'] = item['data'] if 'data' in item else {}
        return item


notification_schema_many = NotificationSchema(many=True, only=('id', 'name', 'description', 'receiver', 'emiter', 'viewed'))
notification_schema = NotificationSchema(many=False)
