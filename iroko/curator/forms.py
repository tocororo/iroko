from __future__ import absolute_import, print_function
from flask_wtf import FlaskForm
from flask_babelex import lazy_gettext as _
<<<<<<< HEAD
from wtforms import IntegerField, TextAreaField, StringField, SelectField, SelectMultipleField, HiddenField, validators
from wtforms.widgets import HiddenInput, ListWidget, CheckboxInput
from iroko.sources.models import Sources, TermSources, SourcesType, HarvestType
=======
from wtforms import IntegerField, StringField, SelectField, SelectMultipleField, HiddenField, validators
from wtforms.widgets import HiddenInput
from iroko.sources.models import Source, TermSources, SourcesType, HarvestType
>>>>>>> 65e8cb1646213fd6cabdfa3420000ca390896da8
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
            message = u'this element already exists'
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
        'Name',
        validators=[validators.DataRequired()]
    )
    description = StringField(
        'Description'
    )
    vocabulary = SelectField(
        'Vocabulary',
        validators=[validators.DataRequired()],
        coerce=int
    )
    parent = SelectField(
        'Parent',
        coerce=int
    )

    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__()
        self.vocabulary.choices=[(choice.id, choice.name) for choice in Vocabulary.query.all()]
        self.parent.choices=[(0,_('None'))]+[(choice.id, choice.name) for choice in Term.query.order_by('name').all()]
     


class SourceForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[validators.DataRequired()]
    )
    source_type = SelectField(
        'Source Type',
        validators=[validators.DataRequired()],        
        choices=[(choice.name, choice.value) for choice in SourcesType]
    )    
    harvest_type = SelectField(
        'Harvest Type',
        validators=[validators.DataRequired()],        
        choices=[(choice.name, choice.value) for choice in HarvestType]  
    )
    harvest_endpoint = StringField(
        'Harvest Endpoint'
    )
    data = TextAreaField(
        'Data'
    )
    terms = MultiCheckboxField(
        'Terms', 
        validators=[validators.Required(message='Please tick at least a term')],
        coerce=int
    )
    
    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__()
        self.terms.choices=[(choice.id, choice.name) for choice in Term.query.all()]
