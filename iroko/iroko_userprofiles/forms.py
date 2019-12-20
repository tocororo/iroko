"""Forms for user profiles."""

from __future__ import absolute_import, print_function

from flask_babelex import lazy_gettext as _
from flask_login import current_user
from flask_security.forms import email_required, email_validator, \
    unique_user_email
from flask_wtf import FlaskForm
from sqlalchemy.orm.exc import NoResultFound
from wtforms import FormField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, StopValidation, \
    ValidationError    

from invenio_userprofiles.api import current_userprofile 
from .models import IrokoUserProfile
from invenio_userprofiles.validators import USERNAME_RULES, validate_username
from invenio_userprofiles.forms import strip_filter, current_user_email, ProfileForm, _update_with_csrf_disabled



class IrokoProfileForm(ProfileForm):
    """Form for editing user profile."""    
    
    extra = StringField(
        # NOTE: Form label
        _('Extra'),
        filters=[strip_filter], )
    


def register_form_factory(Form):
    """Factory for creating an extended user registration form."""
    class CsrfDisabledIrokoProfileForm(IrokoProfileForm):
        """Subclass of ProfileForm to disable CSRF token in the inner form.

        This class will always be a inner form field of the parent class
        `Form`. The parent will add/remove the CSRF token in the form.
        """

        def __init__(self, *args, **kwargs):
            """Initialize the object by hardcoding CSRF token to false."""
            kwargs = _update_with_csrf_disabled(kwargs)
            super(CsrfDisabledIrokoProfileForm, self).__init__(*args, **kwargs)

    class RegisterForm(Form):
        """RegisterForm extended with UserProfile details."""

        profile = FormField(CsrfDisabledIrokoProfileForm, separator='.')

    return RegisterForm


def confirm_register_form_factory(Form):
    """Factory for creating a confirm register form."""
    class CsrfDisabledIrokoProfileForm(IrokoProfileForm):
        """Subclass of ProfileForm to disable CSRF token in the inner form.

        This class will always be a inner form field of the parent class
        `Form`. The parent will add/remove the CSRF token in the form.
        """

        def __init__(self, *args, **kwargs):
            """Initialize the object by hardcoding CSRF token to false."""
            kwargs = _update_with_csrf_disabled(kwargs)
            super(CsrfDisabledIrokoProfileForm, self).__init__(*args, **kwargs)

    class ConfirmRegisterForm(Form):
        """RegisterForm extended with UserProfile details."""

        profile = FormField(CsrfDisabledIrokoProfileForm, separator='.')

    return ConfirmRegisterForm


