# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

"""Forms for user profiles."""

from __future__ import absolute_import, print_function

from flask_admin.form.widgets import Select2Widget
from flask_babelex import lazy_gettext as _
from flask_login import current_user
from flask_security.forms import (
    email_required, email_validator,
    unique_user_email,
    )
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from sqlalchemy.orm.exc import NoResultFound
from wtforms import FormField, StringField, SubmitField, TextAreaField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import (
    DataRequired, EqualTo, StopValidation,
    ValidationError,
    )

from iroko.vocabularies.api import Terms
from .api import current_userprofile, current_userprofile_json_metadata
from .models import UserProfile
from .validators import USERNAME_RULES, validate_username


# photos = UploadSet('photos', IMAGES)


def strip_filter(text):
    """Filter for trimming whitespace.

    :param text: The text to strip.
    :returns: The stripped text.
    """
    return text.strip() if text else text


def current_user_email(form, field):
    """Field validator to stop validation if email wasn't changed."""
    if current_user.email == field.data:
        raise StopValidation()


class ProfileForm(FlaskForm):
    """Form for editing user profile."""

    username = StringField(
        # NOTE: Form field label
        _('Username'),
        # NOTE: Form field help text
        description=_(
            'Required. %(username_rules)s',
            username_rules=USERNAME_RULES
            ),
        validators=[DataRequired(message=_('Username not provided.'))],
        filters=[strip_filter], )

    full_name = StringField(
        # NOTE: Form label
        _('Full name'),
        filters=[strip_filter], )

    avatar = FileField(
        _(
            'Avatar'
            ),
        description=_('An imagen for representing yourself')
        )

    biography = TextAreaField(
        _('Biography'),
        description=_('Short description of your biography'),
        validators=[validators.DataRequired()]
        )

    institution = QuerySelectField(
        label=_('Institution'),
        query_factory=lambda: Terms.get_terms_by_vocabulary_name('institutions'),
        widget=Select2Widget(),
        allow_blank=True,
        blank_text=_('Select Institution')
        )

    institution_rol = StringField(
        _('Role'),
        description=_('Role in the Institution'),
        filters=[strip_filter], )

    def validate_username(form, field):
        """Wrap username validator for WTForms."""
        try:
            validate_username(field.data)
        except ValueError as e:
            raise ValidationError(e)

        try:
            user_profile = UserProfile.get_by_username(field.data)
            if current_userprofile.is_anonymous or \
                (current_userprofile.user_id != user_profile.user_id and
                 field.data != current_userprofile.username):
                # NOTE: Form validation error.
                raise ValidationError(_('Username already exists.'))
        except NoResultFound:
            return

    def __init__(self, formdata=None, **kwargs):
        super(ProfileForm, self).__init__(formdata, **kwargs)
        if not current_userprofile.is_anonymous and current_userprofile_json_metadata:
            msg, institution = Terms.get_term_by_id(
                current_userprofile_json_metadata["institution_id"]
                )
            if institution:
                self.institution.data = institution


class EmailProfileForm(ProfileForm):
    """Form to allow editing of email address."""

    email = StringField(
        # NOTE: Form field label
        _('Email address'),
        filters=[lambda x: x.lower() if x is not None else x, ],
        validators=[
            email_required,
            current_user_email,
            email_validator,
            unique_user_email,
            ],
        )

    email_repeat = StringField(
        # NOTE: Form field label
        _('Re-enter email address'),
        # NOTE: Form field help text
        description=_('Please re-enter your email address.'),
        filters=[lambda x: x.lower() if x else x, ],
        validators=[
            email_required,
            # NOTE: Form validation error.
            EqualTo('email', message=_('Email addresses do not match.'))
            ]
        )


class VerificationForm(FlaskForm):
    """Form to render a button to request email confirmation."""

    # NOTE: Form button label
    send_verification_email = SubmitField(_('Resend verification email'))


def register_form_factory(Form):
    """Factory for creating an extended user registration form."""

    class CsrfDisabledProfileForm(ProfileForm):
        """Subclass of ProfileForm to disable CSRF token in the inner form.

        This class will always be a cinner form field of the parent class
        `Form`. The parent will add/remove the CSRF token in the form.
        """

        def __init__(self, *args, **kwargs):
            """Initialize the object by hardcoding CSRF token to false."""
            kwargs = _update_with_csrf_disabled(kwargs)
            super(CsrfDisabledProfileForm, self).__init__(*args, **kwargs)

    class RegisterForm(Form):
        """RegisterForm extended with UserProfile details."""

        profile = FormField(CsrfDisabledProfileForm, separator='.')

    return RegisterForm


def confirm_register_form_factory(Form):
    """Factory for creating a confirm register form."""

    class CsrfDisabledProfileForm(ProfileForm):
        """Subclass of ProfileForm to disable CSRF token in the inner form.

        This class will always be a inner form field of the parent class
        `Form`. The parent will add/remove the CSRF token in the form.
        """

        def __init__(self, *args, **kwargs):
            """Initialize the object by hardcoding CSRF token to false."""
            kwargs = _update_with_csrf_disabled(kwargs)
            super(CsrfDisabledProfileForm, self).__init__(*args, **kwargs)

    class ConfirmRegisterForm(Form):
        """RegisterForm extended with UserProfile details."""

        profile = FormField(CsrfDisabledProfileForm, separator='.')

    return ConfirmRegisterForm


def _update_with_csrf_disabled(d=None):
    """Update the input dict with CSRF disabled depending on WTF-Form version.

    From Flask-WTF 0.14.0, `csrf_enabled` param has been deprecated in favor of
    `meta={csrf: True/False}`.
    """
    if d is None:
        d = {}

    import flask_wtf
    from pkg_resources import parse_version
    supports_meta = parse_version(flask_wtf.__version__) >= parse_version(
        "0.14.0"
        )
    if supports_meta:
        d.setdefault('meta', {})
        d['meta'].update({'csrf': False})
    else:
        d['csrf_enabled'] = False
    return d
