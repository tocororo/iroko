#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, print_function

from flask_babelex import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, validators
from wtforms.widgets import ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class FaqForm(FlaskForm):
    question = StringField(
        _('Question'),
        description=_('Common question people can ask theirself'),
        validators=[validators.DataRequired()]
    )
    answer = TextAreaField(
        _('Answer'),
        description=_('A sumarized answer for that question')
    )

    # def validate_name(self, field):
    #     if Vocabulary.query.filter_by(identifier=field.data).first():
    #         raise validators.ValidationError(_('Name must not exist'))
