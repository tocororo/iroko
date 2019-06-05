from __future__ import absolute_import, print_function
from flask_wtf import FlaskForm
from flask_babelex import lazy_gettext as _
from wtforms import IntegerField, StringField, SelectField, SelectMultipleField, HiddenField, TextAreaField, validators
from wtforms.widgets import HiddenInput, ListWidget, CheckboxInput
from iroko.sources.models import Source, TermSources, SourcesType, HarvestType
from iroko.taxonomy.models import Vocabulary, Term
from invenio_db import db


class MultiCheckboxField(SelectMultipleField):
    widget			= ListWidget(prefix_label=False)
    option_widget	= CheckboxInput()


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
        validators=[validators.DataRequired(), Unique(Vocabulary, Vocabulary.name)]
    )
    description = StringField(
        _('Description'),
        description=_('Optional explanation for the vocabulary')
    )
    
    # def validate_name(self, field):
    #     if Vocabulary.query.filter_by(name=field.data).first():
    #         raise validators.ValidationError(_('Name must not exist'))


class TermForm(FlaskForm):    
    name = StringField(
        _('Name'),
        validators=[validators.DataRequired()]
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
        validators=[validators.DataRequired()],
        id='group',
        coerce=int
    )
    parent = SelectField(
        _('Parent'),
        coerce=int
    )

    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__()
        group_mes_vocab = Vocabulary.query.filter_by(name='grupo_mes').first()
        
        self.vocabulary.choices=[(choice.id, choice.name) for choice in Vocabulary.query.all()]
        self.group.choices=[(choice.id, choice.name) for choice in Term.query.filter_by(vocabulary_id=group_mes_vocab.id).all()]
        self.parent.choices=[(0,_('None'))]+[(choice.id, choice.name) for choice in Term.query.order_by('name').all()]
     


class SourceForm(FlaskForm):
    name = StringField(
        _('Name'),
        validators=[validators.DataRequired()]
    )
    source_type = SelectField(
        _('Source Type'),
        validators=[validators.DataRequired()],        
        choices=[(choice.name, choice.value) for choice in SourcesType]
    )    
    repo_harvest_type = SelectField(
        _('Harvest Type'),
        validators=[validators.DataRequired()],        
        choices=[(choice.name, choice.value) for choice in HarvestType]  
    )
    repo_harvest_endpoint = StringField(
        _('Harvest Endpoint')
    )
    data = TextAreaField(
        _('Data')
    )
    terms = MultiCheckboxField(
        _('Terms'), 
        validators=[validators.Required(message=_('Please tick at least a term'))],
        coerce=int
    )
    
    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__()
        self.terms.choices=[(choice.id, choice.name) for choice in Term.query.all()]
