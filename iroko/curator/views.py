
"""Iroko sources api views."""

from __future__ import absolute_import, print_function
from flask import Blueprint, request, render_template, flash, url_for, redirect
from flask_login import login_required
from flask_babelex import lazy_gettext as _
from iroko.sources.models import Sources, HarvestType, SourcesType, TermSources
from iroko.taxonomy.models import Vocabulary, Term
from iroko.sources.marshmallow import sources_schema, sources_schema_full, source_schema_full
from os import listdir, path
from .forms import VocabularyForm, TermForm, SourceForm
from .api import create_vocabulary
from invenio_db import db
import uuid
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user


blueprint = Blueprint(
    'iroko_curator',
    __name__,
    url_prefix='/curator',
    
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/add/vocabulary', methods=['GET', 'POST'])
@login_required
def add_vocabulary():
    """The create view."""
    form = VocabularyForm()
    # if the form is submitted and valid
    if form.validate_on_submit():       
        new_vocab = Vocabulary()
        if form.name.data:
            new_vocab.name = form.name.data
        if form.description.data:
            new_vocab.description = form.description.data
        
        db.session.add(new_vocab)
        db.session.commit()

        flash(_('Vocabulary added'), 'info')
        return redirect(url_for('iroko_curator.add_vocabulary'))

    return render_template('add_vocabulary.html', form=form)


@blueprint.route('/add/term', methods=['GET', 'POST'])
@login_required
def add_term():
    """The create view."""
    form = TermForm()       

    # if the form is submitted and valid
    if form.validate_on_submit():        
        new_term = Term()
        form.parent.data
        if form.name.data:
            new_term.name = form.name.data
        if form.description.data:
            new_term.description = form.description.data
        if form.vocabulary.data:
            new_term.vocabulary_id = form.vocabulary.data
        if form.parent.data and form.parent.data != 0:
            new_term.parent_id = form.parent.data 
        
        form.terms.data
        
        db.session.add(new_term)
        db.session.commit()

        flash(_('Term added'), 'info')
        return redirect(url_for('iroko_curator.add_term'))

    return render_template('add_term.html', form=form)


@blueprint.route('/add/source', methods=['GET', 'POST'])
@login_required
def add_source():
    """The create view."""
    form = SourceForm()    

    # if the form is submitted and valid
    if form.validate_on_submit():        
        new_source = Sources()
        
        if form.name.data:
            new_source.name = form.name.data
        if form.source_type.data:
            new_source.source_type = SourcesType[form.source_type.data]
        if form.harvest_type.data:
            new_source.harvest_type = HarvestType[form.harvest_type.data]
        if form.harvest_endpoint.data:
            new_source.harvest_endpoint_id = form.harvest_endpoint.data 
        print(form.terms.data)

        # for term in form.terms.data:
        #     new_source

        db.session.add(new_source)
        db.session.commit()

        flash(_('Source added'), 'info')
        return redirect(url_for('iroko_curator.add_source'))

    return render_template('add_source.html', form=form)


@blueprint.route('/edit/vocabulary/<id>', methods=['GET', 'POST'])
@login_required
def edit_vocabulary(id=None):    
    #security quiestiong here
    print(current_user.has_role('curator'))

    vocab = Vocabulary.query.get_or_404(id)
    form = VocabularyForm()

    if request.method == 'GET':        
        form.id.data = vocab.id
        form.name.data = vocab.name
        form.description.data = vocab.description

    if form.validate_on_submit():
        # changes = {}
        # if form.name.data and form.name.data != vocab.name:
        #     changes['name'] = form.name.data
        # if form.description.data and form.description.data != vocab.description:
        #     changes['description'] = form.description.data        
        #db.session.query(Vocabulary).filter(Vocabulary.id == id).update(changes)
        
        vocab.name = form.name.data
        vocab.description = form.description.data
        
        db.session.commit()

        flash(_('Vocabulary changed'), 'info')
        return redirect(url_for('iroko_curator.add_vocabulary'))    
        
    return render_template('edit_vocabulary.html', id=id, form=form)


@blueprint.route('/edit/term/<id>', methods=['GET', 'POST'])
@login_required
def edit_term(id=None):
    #security quiestiong here

    aux_term = Term.query.get_or_404(id)
    form = TermForm()

    if request.method == 'GET':        
        # form.id.data = aux_term.id
        form.name.data = aux_term.name
        form.description.data = aux_term.description
        form.vocabulary.data = aux_term.vocabulary_id
        form.parent.data = aux_term.parent_id
        

    if form.validate_on_submit():        
        aux_term.name = form.name.data
        aux_term.description = form.description.data
        aux_term.vocabulary_id = form.vocabulary.data
        
        if form.parent.data and form.parent.data != 0:
            aux_term.parent_id = form.parent.data
        else:
            aux_term.parent_id = None
        
        db.session.commit()

        flash(_('Term changed'), 'info')
        return redirect(url_for('iroko_curator.add_term'))    
        
    return render_template('edit_term.html', id=id, form=form)


@blueprint.route('/edit/source/<id>', methods=['GET', 'POST'])
@login_required
def edit_source(id=None):
    #security quiestiong here

    aux_source = Sources.query.get_or_404(id)
    form = SourceForm()

    if request.method == 'GET':        
        # form.id.data = aux_term.id
        form.name.data = aux_source.name
        form.source_type.data = aux_source.source_type
        form.harvest_type.data = aux_source.harvest_type
        form.harvest_endpoint.data = aux_source.harvest_endpoint
        #form.terms.choices = [(tm.term_id, tm.term.name) for tm in  TermSources.query.filter_by(sources_id=id)]
    
    if form.validate_on_submit():        
        aux_source.name = form.name.data
        aux_source.source_type = form.source_type.data
        aux_source.harvest_type = form.harvest_type.data
        aux_source.harvest_endpoint = form.harvest_endpoint.data    

                
        db.session.commit()

        flash(_('Source changed'), 'info')
        return redirect(url_for('iroko_curator.add_source'))    
        
    return render_template('edit_source.html', id=id, form=form)

    

