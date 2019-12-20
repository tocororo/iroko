
"""API for user profiles."""

from __future__ import absolute_import, print_function

from flask import g
from flask_security import current_user
from werkzeug.local import LocalProxy

from iroko.iroko_userprofiles.models import IrokoUserProfile
from invenio_userprofiles.models import AnonymousUserProfile


def _get_current_userprofile():
    """Get current user profile.

    .. note:: If the user is anonymous, then a
        :class:`invenio_userprofiles.models.AnonymousUserProfile` instance is
        returned.

    :returns: The :class:`iroko.irokouserprofiles.models.IrokoUserProfile` instance.
    """
    if current_user.is_anonymous:
        return AnonymousUserProfile()

    profile = g.get(
        'userprofile',
        IrokoUserProfile.get_by_userid(current_user.get_id()))

    if profile is None:
        profile = IrokoUserProfile(user_id=int(current_user.get_id()))
        g.userprofile = profile
    return profile

current_userprofile = LocalProxy(lambda: _get_current_userprofile())
"""Proxy to the user profile of the currently logged in user."""
