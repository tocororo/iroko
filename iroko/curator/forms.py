from __future__ import absolute_import, print_function
from flask_wtf import FlaskForm
from flask_babelex import lazy_gettext as _
from wtforms import StringField, SelectField, SelectMultipleField, validators
from iroko.taxonomy.models import Vocabulary, Term
from iroko.sources.models import Sources, TermSources, SourcesType, HarvestType



class VocabularyForm(FlaskForm):
    name = StringField(
        _('Name'), 
        description=_('Name for the new vocabulary'), 
        validators=[validators.DataRequired()]
    )
    description = StringField(
        _('Description'),
        description=_('Optional explanation for the vocabulary')
    )
    
    def validate_name(form, field):
        if Vocabulary.query.filter_by(name=field.data).first():
            raise validators.ValidationError(_('Name must not exist'))


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
        # coerce='Integer',
        # choices=[(choice.id, choice.name) for choice in Vocabulary.query.all()]
    )
    parent = SelectField(
        'Parent' ,
        # coerce='Integer',
        # choices=[(choice.id, choice.name) for choice in Term.query.all()]
    )   


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
    
         
