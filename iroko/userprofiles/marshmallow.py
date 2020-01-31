from marshmallow import Schema, fields, ValidationError, pre_load
from invenio_records_rest.schemas.fields import DateString
from iroko.userprofiles.models import UserProfile
from invenio_db import db


class UserProfilesSchema(Schema):

    biography = fields.Str()
    institution_id = fields.Integer()

userprofile_schema_many = UserProfilesSchema(many=True)
userprofile_schema = UserProfilesSchema()
