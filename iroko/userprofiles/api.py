# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API for user profiles."""

from __future__ import absolute_import, print_function

from flask import g
from flask_security import current_user
from werkzeug.local import LocalProxy
from marshmallow import ValidationError
from .models import AnonymousUserProfile, UserProfile
from .marshmallow import userprofile_schema



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
        UserProfile.get_by_userid(current_user.get_id()))

    if profile is None:
        profile = UserProfile(user_id=int(current_user.get_id()))
        g.userprofile = profile
    return profile


def _get_current_userprofile_json_metadata():
    if current_userprofile.json_metadata:
        try:
            data = userprofile_schema.loads(current_userprofile.json_metadata)
        except ValidationError as err:
            pass
    
    return None


current_userprofile = LocalProxy(lambda: _get_current_userprofile())
"""Proxy to the user profile of the currently logged in user."""

current_userprofile_json_metadata = LocalProxy(lambda: _get_current_userprofile_json_metadata())
