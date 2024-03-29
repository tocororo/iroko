#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, print_function

from flask_babelex import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField, SelectField, SelectMultipleField, StringField, TextAreaField, validators,
    )
from wtforms.widgets import CheckboxInput, HiddenInput, ListWidget

from iroko.sources.models import SourceType
from iroko.utils import IrokoVocabularyIdentifiers
from iroko.vocabularies.models import Term, Vocabulary


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class Unique(object):
    """ validator that checks field uniqueness """

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = _('this element already exists')
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if 'id' in form:
            id = form.id.data
        else:
            id = None
        if check and (id is None or id != check.id):
            raise validators.ValidationError(self.message)


class VocabularyForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    name = StringField(
        _('Name'),
        description=_('Name for the new vocabulary'),
        validators=[validators.DataRequired(), Unique(Vocabulary, Vocabulary.identifier)]
        )
    description = StringField(
        _('Description'),
        description=_('Optional explanation for the vocabulary')
        )

    # def validate_name(self, field):
    #     if Vocabulary.query.filter_by(identifier=field.data).first():
    #         raise validators.ValidationError(_('Name must not exist'))


class TermForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    name = StringField(
        _('Name'),
        validators=[validators.DataRequired(), Unique(Term, Term.identifier)]
        )
    description = StringField(
        _('Description')
        )
    vocabulary = SelectField(
        _('Vocabulary'),
        validators=[validators.DataRequired()],
        id='vocabulary',
        coerce=int
        )
    group = SelectField(
        _('MES Group'),
        id='group',
        coerce=int
        )
    parent = SelectField(
        _('Parent'),
        coerce=int
        )

    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__()
        group_mes_vocab = Vocabulary.query.filter_by(
            identifier=IrokoVocabularyIdentifiers.INDEXES_CLASIFICATION.value
            ).first()

        self.vocabulary.choices = [(choice.id, choice.name) for choice in Vocabulary.query.all()]
        self.group.choices = [(0, _('None'))] + [(choice.id, choice.name) for choice in
                                                 Term.query.filter_by(
                                                     vocabulary_id=group_mes_vocab.identifier
                                                     ).all()]
        self.parent.choices = [(0, _('None'))] + [(choice.id, choice.name) for choice in
                                                  Term.query.order_by('name').all()]

    def validate_group(self, field):
        data_bases = Vocabulary.query.filter_by(
            identifier=IrokoVocabularyIdentifiers.INDEXES.value
            ).first()
        if self.vocabulary.data == data_bases.id and field.data == 0:  # 4 is the data_bases id
            raise validators.ValidationError(_('You must asign a MES group if database'))
        if field.data != 0 and not Term.query.filter_by(id=field.data).first():
            raise validators.ValidationError(_('You must select a valid MES group'))


class SourceForm(FlaskForm):
    name = StringField(
        _('Name'),
        validators=[validators.DataRequired()]
        )
    source_type = SelectField(
        _('Source Type'),
        validators=[validators.DataRequired()],
        choices=[(choice.name, choice.value) for choice in SourceType]
        )
    # repo_harvest_type = SelectField(
    #     _('Harvest Type'),
    #     validators=[validators.DataRequired()],
    #     choices=[(choice.name, choice.value) for choice in [HarvestType]]
    # )
    repo_harvest_endpoint = StringField(
        _('Harvest Endpoint')
        )
    data = TextAreaField(
        _('Data')
        )
    terms = MultiCheckboxField(
        _('Terms'),
        validators=[validators.DataRequired(message=_('Please tick at least a term'))],
        coerce=int
        )

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__()
        self.terms.choices = [(choice.id, choice.name) for choice in Term.query.all()]
