# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Database models for user profiles."""

from __future__ import absolute_import, print_function

from invenio_accounts.models import User
from invenio_db import db
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils.types import JSONType

from iroko.sources.api import SourceRecord
from .validators import validate_username


class AnonymousUserProfile():
    """Anonymous user profile."""
    json_metadata = db.Column(JSONType)

    @property
    def is_anonymous(self):
        """Return whether this UserProfile is anonymous."""
        return True


class UserProfile(db.Model):
    """User profile model.

    Stores a username, display name (case sensitive version of username) and a
    full name for a user.
    """

    __tablename__ = 'userprofiles_userprofile'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
        primary_key=True
    )
    """Foreign key to :class:`~invenio_accounts.models.User`."""

    user = db.relationship(
        User, backref=db.backref(
            'profile', uselist=False, cascade='all, delete-orphan')
    )
    """User relationship."""

    _username = db.Column('username', db.String(255), unique=True)
    """Lower-case version of username to assert uniqueness."""

    _displayname = db.Column('displayname', db.String(255))
    """Case preserving version of username."""

    full_name = db.Column(db.String(255), nullable=False, default='')
    """Full name of person."""

    json_metadata = db.Column(JSONType)
    """Store metadata in JSON format."""

    @hybrid_property
    def username(self):
        """Get username."""
        return self._displayname

    @username.setter
    def username(self, username):
        """Set username.

        .. note:: The username will be converted to lowercase. The display name
            will contain the original version.
        """
        validate_username(username)
        self._username = username.lower()
        self._displayname = username

    @classmethod
    def get_by_username(cls, username):
        """Get profile by username.

        :param username: A username to query for (case insensitive).
        """
        return cls.query.filter(
            UserProfile._username == username.lower()
        ).one()

    @classmethod
    def get_by_userid(cls, user_id):
        """Get profile by user identifier.

        :param user_id: Identifier of a :class:`~invenio_accounts.models.User`.
        :returns: A :class:`~invenio_userprofiles.models.UserProfile` instance
            or ``None``.
        """
        return cls.query.filter_by(user_id=user_id).one_or_none()

    @classmethod
    def get_or_create_by_userid(cls, user_id):
        """Get profile by user identifier.

        :param user_id: Identifier of a :class:`~invenio_accounts.models.User`.
        :returns: A :class:`~invenio_userprofiles.models.UserProfile` instance
            or ``None``.
        """
        profile = cls.query.filter_by(user_id=user_id).one_or_none()
        if not profile:
            user = User.query.filter_by(id=user_id).one_or_none()
            if not user:
                raise Exception('Cannot create profile. Not user_id={0}'.format(user_id))
            profile = cls()
            profile.user_id = user.id
            db.session.add(profile)
            db.session.commit()

        return profile



    @property
    def is_anonymous(self):
        """Return whether this UserProfile is anonymous."""
        return False

    @classmethod
    def add_source_to_user_profile(cls, user_id, source_uuid, role):

        print('add_source_to_user_profile', user_id, source_uuid, role)
        user_profile = cls.get_or_create_by_userid(user_id)
        if not user_profile:
            raise Exception('No user_id={0}'.format(user_id))

        pid, source = SourceRecord.get_source_by_pid(source_uuid)
        if not pid or not source:
            raise Exception('No source_uuid={0}'.format(source_uuid))

        add = True
        if user_profile.json_metadata:
            data = dict(user_profile.json_metadata)
        else:
            data = dict()
        if 'sources' not in data:
            data['sources'] = []
        for s in data['sources']:
            if s['source_uuid'] == source_uuid:
                s['role'] = role
                add = False
        if add:
            data['sources'].append({'source_uuid': source_uuid, 'role': role})
        user_profile.json_metadata = dict(data)
        db.session.commit()
        print(user_profile, user_profile.json_metadata)

    @classmethod
    def remove_source_from_user_profile(cls, user_id, source_uuid):
        user_profile = cls.get_or_create_by_userid(user_id)
        if not user_profile:
            raise Exception('No user_id={0}'.format(user_id))
        sources=[]
        data = dict(user_profile.json_metadata)
        if 'sources' not in data:
            data['sources'] = []
        for s in data['sources']:
            if s['source_uuid'] != source_uuid:
                sources.append(s)
        data['sources'] = sources
        user_profile.json_metadata = dict(data)
        db.session.commit()



@event.listens_for(User, 'init')
def on_user_init(target, args, kwargs):
    """Provide hook on :class:`~invenio_accounts.models.User` initialization.

    Automatically convert a dict to a
    :class:`~.UserProfile` instance. This is needed
    during e.g. user registration where Flask-Security will initialize a
    user model with all the form data (which when Invenio-UserProfiles is
    enabled includes a ``profile`` key). This will make the user creation fail
    unless we convert the profile dict into a :class:`~.UserProfile` instance.
    """
    profile = kwargs.pop('profile', None)
    if profile is not None and not isinstance(profile, UserProfile):
        profile = UserProfile(**profile)
        if kwargs.get('id'):
            profile.user_id = kwargs['id']
        kwargs['profile'] = profile
