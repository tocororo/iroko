from __future__ import absolute_import, print_function
from flask_wtf import FlaskForm
from flask_babelex import lazy_gettext as _
from wtforms import IntegerField, StringField, SelectField, SelectMultipleField, HiddenField, TextAreaField, validators
from wtforms.widgets import HiddenInput, ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget			= ListWidget(prefix_label=False)
    option_widget	= CheckboxInput()


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
    #     if Vocabulary.query.filter_by(name=field.data).first():
    #         raise validators.ValidationError(_('Name must not exist'))

