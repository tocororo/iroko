
"""Iroko sources api views."""

from __future__ import absolute_import, print_function
from flask import Blueprint, request, render_template
from flask_login import login_required
from iroko.sources.models import Sources, HarvestType, SourcesType
from iroko.taxonomy.models import Vocabulary, Term
from iroko.sources.marshmallow import sources_schema, sources_schema_full, source_schema_full
from os import listdir, path
from .forms import VocabularyForm, TermForm, SourceForm
from .api import create_vocabulary
from invenio_db import db


blueprint = Blueprint(
    'iroko_curator',
    __name__,
    url_prefix='/curator',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/add/vocabulary')
@login_required
def add_vocabulary():
    """The create view."""
    form = VocabularyForm()
    # if the form is submitted and valid
    if form.validate_on_submit():
        # set the owner as the current logged in user
        #owner = int(current_user.get_id())
        # create the record
        # create_record(
        #   dict(
        #     name=form.name.data,
        #     description=form.description.data,
        #     owner=owner,
        #   )
        # )
        # redirect to the success page
        new_vocab = Vocabulary()
        if form.name.data:
            new_vocab.name = form.name.data
        if form.description.data:
            new_vocab.description = form.description.data
        
        db.session.add(new_vocab)
        db.session.commit()

    return render_template('curator/add_vocabulary.html', form=form)


@blueprint.route('/add/term')
@login_required
def add_term():
    """The create view."""
    form = TermForm()    
    # if the form is submitted and valid
    if form.validate_on_submit():
        # set the owner as the current logged in user
        #owner = int(current_user.get_id())
        # create the record
        # create_record(
        #   dict(
        #     name=form.name.data,
        #     description=form.description.data,
        #     owner=owner,
        #   )
        # )
        # redirect to the success page
        new_term = Term()
        if form.uuid.data:
            new_term.uuid = form.uuid.data
        if form.name.data:
            new_term.name = form.name.data
        if form.description.data:
            new_term.description = form.description.data
        if form.vocabulary.data:
            new_term.vocabulary_id = form.vocabulary.data
        if form.parent.data:
            new_term.parent_id = form.parent.data 
        
        db.session.add(new_term)
        db.session.commit()

    return render_template('curator/add_vocabulary.html', form=form)


@blueprint.route('/add/source')
@login_required
def add_source():
    """The create view."""
    form = TermForm()    
    # if the form is submitted and valid
    if form.validate_on_submit():
        # set the owner as the current logged in user
        #owner = int(current_user.get_id())
        # create the record
        # create_record(
        #   dict(
        #     name=form.name.data,
        #     description=form.description.data,
        #     owner=owner,
        #   )
        # )
        # redirect to the success page
        new_source = Sources()
        if form.uuid.data:
            new_source.uuid = form.uuid.data
        if form.name.data:
            new_source.name = form.name.data
        if form.source_type.data:
            new_source.source_type = SourcesType[form.source_type.data]
        if form.harvest_type.data:
            new_source.harvest_type = HarvestType[form.harvest_type.data]
        if form.harvest_endpoint.data:
            new_source.harvest_endpoint_id = form.harvest_endpoint.data 
        
        db.session.add(new_source)
        db.session.commit()
        
    return render_template('curator/add_source.html', form=form)


@blueprint.route('/edit/term/<id>')
@login_required
def edit_term():
    # the form stuffs...
    pass


@blueprint.route('/edit/vocabulary/<id>')
@login_required
def edit_vocabulary():
    # the form stuffs...
    pass
