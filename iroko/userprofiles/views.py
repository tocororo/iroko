# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Invenio module that adds userprofiles to the platform."""

from __future__ import absolute_import, print_function

import base64
import os

from flask import Blueprint, current_app, flash, render_template, request
from flask_babelex import lazy_gettext as _
from flask_breadcrumbs import register_breadcrumb
from flask_login import current_user, login_required
from flask_menu import register_menu
from flask_security.confirmable import send_confirmation_instructions
from invenio_db import db
from werkzeug.utils import secure_filename

from iroko.vocabularies.api import Terms
from .api import current_userprofile, current_userprofile_json_metadata
from .forms import (
    EmailProfileForm, ProfileForm, VerificationForm,
    confirm_register_form_factory, register_form_factory,
    )
from .models import UserProfile

blueprint = Blueprint(
    'invenio_userprofiles',
    __name__,
    template_folder='templates',
    )

blueprint_ui_init = Blueprint(
    'invenio_userprofiles_ui_init',
    __name__,
    )


def init_common(app):
    """Post initialization."""
    if app.config['USERPROFILES_EXTEND_SECURITY_FORMS']:
        security_ext = app.extensions['security']
        security_ext.confirm_register_form = confirm_register_form_factory(
            security_ext.confirm_register_form
            )
        security_ext.register_form = register_form_factory(
            security_ext.register_form
            )


@blueprint_ui_init.record_once
def init_ui(state):
    """Post initialization for UI application."""
    app = state.app
    init_common(app)

    # Register blueprint for templates
    app.register_blueprint(
        blueprint, url_prefix=app.config['USERPROFILES_PROFILE_URL']
        )


@blueprint.app_template_filter()
def userprofile(value):
    """Retrieve user profile for a given user id."""
    return UserProfile.get_by_userid(int(value))


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
@register_menu(
    blueprint, 'settings.profile',
    # NOTE: Menu item text (icon replaced by a user icon).
    _('%(icon)s Profile', icon='<i class="fa fa-user fa-fw"></i>'),
    order=0
    )
@register_breadcrumb(
    blueprint, 'breadcrumbs.settings.profile', _('Profile')
    )
def profile():
    """View for editing a profile."""
    # Create forms
    verification_form = VerificationForm(formdata=None, prefix="verification")
    profile_form = profile_form_factory()

    # Process forms
    form = request.form.get('submit', None)
    if form == 'profile':
        handle_profile_form(profile_form)
    elif form == 'verification':
        handle_verification_form(verification_form)

    return render_template(
        current_app.config['USERPROFILES_PROFILE_TEMPLATE'],
        profile_form=profile_form,
        verification_form=verification_form, )


def profile_form_factory():
    """Create a profile form."""
    t_biography = ''
    t_institution = 0
    t_institution_rol = ''
    t_avatar = ''
    if current_userprofile_json_metadata:
        t_biography = current_userprofile_json_metadata[
            "biography"] if "biography" in current_userprofile_json_metadata.keys() else ""
        msg, t_institution = Terms.get_term_by_id(
            current_userprofile_json_metadata[
                "institution_id"]
            ) if "institution_id" in current_userprofile_json_metadata.keys() else 0
        t_institution_rol = current_userprofile_json_metadata[
            "institution_rol"] if "institution_rol" in current_userprofile_json_metadata.keys() \
            else ""
        t_avatar = current_userprofile_json_metadata[
            "avatar"] if "avatar" in current_userprofile_json_metadata.keys() else ""

    if current_app.config['USERPROFILES_EMAIL_ENABLED']:
        return EmailProfileForm(
            formdata=None,
            username=current_userprofile.username,
            full_name=current_userprofile.full_name,
            biography=t_biography,
            institution=t_institution.id if t_institution != 0 else 0,
            avatar=base64.b64decode(str('t_avatar')) if t_avatar != '' else None,
            email=current_user.email,
            email_repeat=current_user.email,
            prefix='profile', )
    else:

        return ProfileForm(
            formdata=None,
            username=current_userprofile.username,
            full_name=current_userprofile.full_name,
            biography=t_biography,
            institution=t_institution.id if t_institution != 0 else 0,
            avatar=base64.b64decode(str('t_avatar')) if t_avatar != '' else None,
            institution_rol=t_institution_rol,
            prefix='profile', )


def handle_verification_form(form):
    """Handle email sending verification form."""
    form.process(formdata=request.form)

    if form.validate_on_submit():
        send_confirmation_instructions(current_user)
        # NOTE: Flash message.
        flash(_("Verification email sent."), category="success")


def handle_profile_form(form):
    """Handle profile update form."""
    form.process(formdata=request.form)
    if form.validate_on_submit():
        email_changed = False
        with db.session.begin_nested():
            # Update profile.
            current_userprofile.username = form.username.data
            current_userprofile.full_name = form.full_name.data
            data = dict()
            data["biography"] = form.biography.data
            data["institution_id"] = form.institution.data.id
            data["institution_rol"] = form.institution_rol.data
            data["avatar"] = ""
            # print("fichero= ", form.avatar.data)

            # print("aquiiiiii", request)

            # if f:
            #     filename = secure_filename(f.filename)
            #     # print("otro= ", filename)

            if form.avatar.data:
                filename = secure_filename(form.avatar.data.filename)
                path_avatar = os.path.join(current_app.config.get('UPLOADED_PHOTOS_DEST'), filename)
                # print("path= ", path_avatar)
                form.avatar.data.save(path_avatar)

                with open(path_avatar, "r") as file_avatar:
                    encoded_avatar = base64.b64encode(file_avatar)
                    data["avatar"] = encoded_avatar

            current_userprofile.json_metadata = data
            ## print(current_userprofile.json_metadata)
            db.session.add(current_userprofile)

            # Update email
            if current_app.config['USERPROFILES_EMAIL_ENABLED'] and \
                form.email.data != current_user.email:
                current_user.email = form.email.data
                current_user.confirmed_at = None
                db.session.add(current_user)
                email_changed = True
        db.session.commit()

        if email_changed:
            send_confirmation_instructions(current_user)
            # NOTE: Flash message after successful update of profile.
            flash(
                _(
                    'Profile was updated. We have sent a verification '
                    'email to %(email)s. Please check it.',
                    email=current_user.email
                    ),
                category='success'
                )
        else:
            # NOTE: Flash message after successful update of profile.
            flash(_('Profile was updated.'), category='success')
