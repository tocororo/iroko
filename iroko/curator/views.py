#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, print_function

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_babelex import lazy_gettext as _
from flask_login import login_required
from invenio_db import db

from iroko.curator.permissions import source_create_permission, vocabulary_create_permission
from iroko.sources.models import Source
from iroko.utils import IrokoVocabularyIdentifiers
from iroko.vocabularies.models import Term, TermClasification, Vocabulary
from .forms import SourceForm, TermForm, VocabularyForm

blueprint = Blueprint(
    'iroko_curator',
    __name__,
    url_prefix='/curator',

    template_folder='templates',
    static_folder='static'
    )


@blueprint.route('/add/vocabulary', methods=['GET', 'POST'])
@login_required
@vocabulary_create_permission.require(http_exception=403)
def add_vocabulary():
    """The create view."""
    form = VocabularyForm()
    # if the form is submitted and valid
    if form.validate_on_submit():
        new_vocab = Vocabulary()
        if form.name.data:
            new_vocab.identifier = form.name.data
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
            new_term.identifier = form.name.data
        if form.description.data:
            new_term.description = form.description.data
        if form.vocabulary.data:
            new_term.vocabulary_id = form.vocabulary.data
        if form.parent.data and form.parent.data != 0:
            new_term.parent_id = form.parent.data

        db.session.add(new_term)
        db.session.flush()

        if new_term.vocabulary.name == 'data_bases' and form.group.data != 0:
            new_group = TermClasification()
            new_group.term_base_id = new_term.id  # id del termino que es base de datos
            new_group.term_group_id = form.group.data  # id del termino del combo que dice el
            # grupo mes
            db.session.add(new_group)

        db.session.commit()

        flash(_('Term added'), 'info')
        return redirect(url_for('iroko_curator.add_term'))

    return render_template('add_term.html', form=form)


@blueprint.route('/add/source', methods=['GET', 'POST'])
@login_required
@source_create_permission.require(http_exception=403)
def add_source():
    """The create view."""
    form = SourceForm()

    # if the form is submitted and valid
    if form.validate_on_submit():
        new_source = Source()

        # if form.name.data:
        #     new_source.name = form.name.data
        # if form.source_type.data:
        #     new_source.source_type = SourceType[form.source_type.data]
        # if form.repo_harvest_type.data:
        #     new_source.repo_harvest_type = HarvestType[form.repo_harvest_type.data]
        # if form.repo_harvest_endpoint.data:
        #     new_source.repo_harvest_endpoint = form.repo_harvest_endpoint.data
        # # print(form.terms.data)

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
    # security questiong here
    # print(current_user.has_role('curator'))

    vocab = Vocabulary.query.get_or_404(id)
    form = VocabularyForm()

    if request.method == 'GET':
        form.id.data = vocab.id
        form.name.data = vocab.identifier
        form.description.data = vocab.description

    if form.validate_on_submit():
        # changes = {}
        # if form.name.data and form.name.data != vocab.identifier:
        #     changes['name'] = form.name.data
        # if form.description.data and form.description.data != vocab.description:
        #     changes['description'] = form.description.data
        # db.session.query(Vocabulary).filter(Vocabulary.id == id).update(changes)

        vocab.identifier = form.name.data
        vocab.description = form.description.data

        db.session.commit()

        flash(_('Vocabulary changed'), 'info')
        return redirect(url_for('iroko_curator.add_vocabulary'))

    return render_template('edit_vocabulary.html', id=id, form=form)


@blueprint.route('/edit/term/<id>', methods=['GET', 'POST'])
@login_required
def edit_term(id=None):
    # security quiestiong here

    aux_term = Term.query.get_or_404(id)
    form = TermForm()

    if request.method == 'GET':
        form.id.data = aux_term.id
        form.name.data = aux_term.name
        form.description.data = aux_term.description
        form.vocabulary.data = aux_term.vocabulary_id
        form.parent.data = aux_term.parent_id

        group = TermClasification.query.filter_by(term_base_id=aux_term.id).first()
        if group:
            form.group.data = group.term_group_id

    if form.validate_on_submit():
        aux_term.name = form.name.data
        aux_term.description = form.description.data

        data_base_vocab = Vocabulary.query.filter_by(
            identifier=IrokoVocabularyIdentifiers.INDEXES.value
            ).first()
        if aux_term.vocabulary_id == data_base_vocab.identifier:
            group = TermClasification.query.filter_by(term_base_id=aux_term.id).first()
            if group:
                if form.vocabulary.data != data_base_vocab.id:
                    # delete the Mes group previously associated
                    db.session.delete(group)
                    db.session.commit()
                else:
                    # cahnge if needed the MES group
                    if group.term_group_id != form.group.data:
                        group.term_group_id = form.group.data
                        db.session.commit()
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
    # security quiestiong here

    aux_source = Source.query.get_or_404(id)
    form = SourceForm()

    if request.method == 'GET':
        # form.id.data = aux_term.id
        form.name.data = aux_source.name
        form.source_type.data = aux_source.source_type
        form.repo_harvest_type.data = aux_source.repo_harvest_type
        form.repo_harvest_endpoint.data = aux_source.repo_harvest_endpoint
        # form.terms.choices = [(tm.term_id, tm.term.name) for tm in
        # TermSources.query.filter_by(sources_id=id)]
        # print(aux_source.source_type)

    if form.validate_on_submit():
        aux_source.name = form.name.data
        aux_source.source_type = form.source_type.data
        aux_source.repo_harvest_type = form.repo_harvest_type.data
        aux_source.repo_harvest_endpoint = form.repo_harvest_endpoint.data
        # print(aux_source.source_type)

        db.session.commit()

        flash(_('Source changed'), 'info')
        return redirect(url_for('iroko_curator.add_source'))

    return render_template('edit_source.html', id=id, form=form)
