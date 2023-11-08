#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from marshmallow import Schema, fields


class UserRolesSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    confirmed_at = fields.Str()
    last_login_at = fields.Str()
    roles = fields.Nested(UserRolesSchema, many=True)


class SourcesRoles(Schema):
    source_uuid = fields.Str(allow_none=True)
    role = fields.Str(allow_none=True)


class UserProfileDataSchema(Schema):
    biography = fields.Str()
    institution_id = fields.Integer()
    institution_rol = fields.Str()
    avatar = fields.Str()
    sources = fields.Nested(SourcesRoles, many=True)


class UserProfilesSchema(Schema):
    _username = fields.Str()
    """Lower-case version of username to assert uniqueness."""

    _displayname = fields.Str()
    """Case preserving version of username."""

    full_name = fields.Str()
    """Full name of person."""

    json_metadata = fields.Nested(UserProfileDataSchema, many=False)

    user = fields.Nested(UserSchema, many=False)


user_schema_many = UserSchema(many=True)

userprofile_schema_many = UserProfilesSchema(many=True)
userprofile_schema = UserProfilesSchema()
