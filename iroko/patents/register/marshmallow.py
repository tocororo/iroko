from marshmallow import Schema, fields, post_load

from iroko.evaluations.models import EvaluationState


class RegisterSchema(Schema):

    id = fields.Int()
    userEmail = fields.Str(required=False, allow_none=True)
    date = fields.DateTime()
    patents = fields.Int()

    @post_load
    def register_load(self, item, **kwargs):
        item['userEmail'] = item['userEmail'] if 'userEmail' in item else ''
        item['date'] = item['date'] if 'date' in item else ''
        item['patents'] = item['patents'] if 'patents' in item else ''
        return item


register_schema_many = RegisterSchema(
    many=True, only=(
        'id', 'userEmail', 'date', 'patents')
    )
register_schema = RegisterSchema(many=False)
