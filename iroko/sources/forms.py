#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, print_function

import json

from flask import current_app
# from flask_wtf.html5 import URLField, EmailField
from flask_babelex import lazy_gettext as _
from flask_wtf import FlaskForm
from invenio_i18n.selectors import get_locale
from wtforms import StringField, SelectMultipleField, validators
from wtforms.fields.html5 import URLField, EmailField
from wtforms.widgets import ListWidget, CheckboxInput, HTMLString, html_params


class MyListWidget(ListWidget):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append('<li class="class="d-flex align-items-baseline"">%s %s</li>' % (subfield.label, subfield()))
            else:
                html.append('<li class="d-flex align-items-baseline">%s %s</li>' % (subfield(), subfield.label))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))


class MultiCheckboxField(SelectMultipleField):
    widget = MyListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class InclusionForm(FlaskForm):
    source = StringField(
        _('Source name'),
        description=_('Name for the journal or repository postulating'),
        validators=[validators.DataRequired()]
    )
    homepage_url = URLField(
        _('Homepage Url'),
        validators=[validators.DataRequired()]
    )
    contact_name = StringField(
        _('Contact name'),
        description=_('Your Full Name'),
        validators=[validators.DataRequired()]
    )
    contact_email = EmailField(
        _('Contact Email'),
        description=_('Email for contacting and processing'),
        validators=[validators.DataRequired()]
    )
    requeriments = MultiCheckboxField(
        _('Inclusion checklist'),
        validators=[validators.DataRequired(message=_('Please tick those who you fullfill'))],
    )

    def __init__(self, *args, **kwargs):
        super(InclusionForm, self).__init__()
        requeriments = {}
        choices = []
        with open(
            current_app.config['INIT_STATIC_JSON_PATH'] + '/' + get_locale() + '/inclusion_requeriments.json') as file:
            requeriments = json.load(file)
            for item in requeriments:
                choices.append((item, requeriments[item]))
        self.requeriments.choices = choices
