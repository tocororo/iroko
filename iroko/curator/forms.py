from __future__ import absolute_import, print_function
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, validators
from iroko.taxonomy.models import Vocabulary, Term
from iroko.sources.models import Sources, TermSources, SourcesType, HarvestType
import uuid



class VocabularyForm(FlaskForm):
    name = StringField(
        'Name', 
        description='Name for the new vocabulary', 
        validators=[validators.DataRequired()]
    )
    description = StringField(
        'Description',
        description='Optional explanation for the vocabulary'        
    )


class TermForm(FlaskForm):
    uuid = StringField(
        'UUID',
        description='Unique identification asigned code',
        default=uuid.uuid4
    )
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
    uuid = StringField(
        'UUID',
        description='Unique identification asigned code',
        default=uuid.uuid4
    )
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
    #data
         
