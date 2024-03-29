# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""API for user profiles."""

from __future__ import absolute_import, print_function

from flask import g
from flask_security import current_user
from marshmallow import ValidationError
from werkzeug.local import LocalProxy

from .marshmallow import userprofile_schema
from .models import AnonymousUserProfile, UserProfile


def _get_current_userprofile():
    """Get current user profile.

    .. note:: If the user is anonymous, then a
        :class:`invenio_userprofiles.models.AnonymousUserProfile` instance is
        returned.

    :returns: The :class:`invenio_userprofiles.models.UserProfile` instance.
    """
    if current_user.is_anonymous:
        return AnonymousUserProfile()

    profile = g.get(
        'userprofile',
        UserProfile.get_by_userid(current_user.get_id())
        )
    # UserProfile.get_or_create_by_userid(current_user.get_id()))

    if profile is None:
        profile = UserProfile(user_id=int(current_user.get_id()))
        g.userprofile = profile
    return profile


def _get_current_userprofile_json_metadata():
    if current_userprofile.json_metadata:
        try:
            data = userprofile_schema.load(current_userprofile)
            return data
        except ValidationError as err:
            pass

    return None


current_userprofile = LocalProxy(lambda: _get_current_userprofile())
"""Proxy to the user profile of the currently logged in user."""

current_userprofile_json_metadata = LocalProxy(lambda: _get_current_userprofile_json_metadata())
