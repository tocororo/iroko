
from __future__ import absolute_import, division, print_function

import json
import os

from flask import current_app
from invenio_db import db
from rdflib import Graph, URIRef
from rdflib.namespace import SKOS

from iroko.sources.miar.api import MiarHarvester
from iroko.sources.models import TermSources
from iroko.utils import IrokoVocabularyIdentifiers, string_as_identifier
from iroko.vocabularies.models import Vocabulary, Term


def init_taxonomy():
    """Init vocabularies"""
    delete_all_vocabs()
    print('delete all vocabs and terms')
#     tax_path = '../../data/taxonomy.json' .
    datadir = current_app.config['IROKO_DATA_DIRECTORY']

    init_cuntries(os.path.join(datadir, 'countries.json'))
    init_unesco(os.path.join(datadir, 'unesco-thesaurus.rdf'))
    # init_indexes()

    path = os.path.join(datadir, 'vocabularies.json')

    with open(path) as f:
        tax = json.load(f)
        # institutions = Vocabulary()
        # institutions.identifier = IrokoVocabularyIdentifiers.CUBAN_INTITUTIONS.value
        # institutions.human_name = 'Instituciones Cubanas'
        # db.session.add(institutions)
        #
        # extra_institutions = Vocabulary()
        # extra_institutions.identifier = IrokoVocabularyIdentifiers.EXTRA_INSTITUTIONS.value
        # extra_institutions.human_name = 'Instituciones sin REUP'
        # db.session.add(extra_institutions)

        # provinces = Vocabulary()
        # provinces.identifier = IrokoVocabularyIdentifiers.CUBAN_PROVINCES.value
        # provinces.human_name = 'Provincias Cubanas'
        # db.session.add(provinces)

        grupo_mes = Vocabulary()
        grupo_mes.identifier = IrokoVocabularyIdentifiers.INDEXES_CLASIFICATION.value
        grupo_mes.human_name = 'Clasificaciones de Bases de Datos e Indizadores'
        db.session.add(grupo_mes)

        licences = Vocabulary()
        licences.identifier = IrokoVocabularyIdentifiers.LICENCES.value
        licences.human_name = 'Licencias'
        db.session.add(licences)

        record_sets = Vocabulary()
        record_sets.identifier = IrokoVocabularyIdentifiers.RECOD_SETS.value
        record_sets.human_name = 'Conjuntos de Articulos'
        db.session.add(record_sets)

        # record_set is clasified as record_type
        record_types = Vocabulary()
        record_types.identifier = IrokoVocabularyIdentifiers.RECORD_TYPES.value
        record_types.human_name = 'Tipos de Articulos'
        db.session.add(record_types)

        db.session.commit()

        # init_vocabulary(tax, 'institutions', institutions)
        # init_vocabulary(tax, 'provinces',provinces)
        init_vocabulary(tax, 'grupo_mes', grupo_mes)
        init_vocabulary(tax, 'licences', licences)


def init_vocabulary(tax, tax_name, vocab):
    """init a vocabulary"""

    for k, term in tax[tax_name].items():
        nterm = Term()
        nterm.identifier = string_as_identifier(term['name'])
        nterm.description = term['name']
        nterm.vocabulary_id = vocab.identifier
        if term['parents'][0] != '0':
            if tax[tax_name][term['parents'][0]]:
                parent_name = string_as_identifier(tax[tax_name][term['parents'][0]]['name'])
                parent = Term.query.filter_by(identifier=parent_name).first()
                nterm.parent_id = parent.id
        db.session.add(nterm)
        db.session.commit()


def init_cuntries(path):
    vocab = Vocabulary()
    vocab.identifier = IrokoVocabularyIdentifiers.COUNTRIES.value
    vocab.human_name = 'Paises'
    db.session.add(vocab)
    db.session.commit()

    with open(path) as f:
        countries = json.load(f)
        for country in countries:
            nterm = Term()
            nterm.identifier = country['key']
            nterm.description = country['text']
            nterm.vocabulary_id = vocab.identifier
            db.session.add(nterm)
        db.session.commit()


def init_unesco(path):

    subjects = Vocabulary()
    subjects.identifier = IrokoVocabularyIdentifiers.SUBJECTS.value
    subjects.human_name = 'Cobertura tematica'
    db.session.add(subjects)

    db.session.commit()

    groups = [
        {
            'name': 'http://vocabularies.unesco.org/thesaurus/domain1',
            'description': 'Educación'
        },{
            'name': 'http://vocabularies.unesco.org/thesaurus/domain2',
            'description': 'Ciencia'
        },{
            'name': 'http://vocabularies.unesco.org/thesaurus/domain3',
            'description': 'Cultura'
        },{
            'name': 'http://vocabularies.unesco.org/thesaurus/domain4',
            'description': 'Ciencias sociales y humanas'
        },{
            'name': 'http://vocabularies.unesco.org/thesaurus/domain5',
            'description': 'Información y comunicación'
        },{
            'name': 'http://vocabularies.unesco.org/thesaurus/domain6',
            'description': 'Política, derecho y economía'
        }
    ]

    graph = Graph()
    graph.load(path)

    for t in groups:
        term = Term()
        term.identifier = t['name']
        term.description = t['description']
        term.vocabulary_id = subjects.identifier
        db.session.add(term)
        db.session.commit()
        _add_group_terms(graph, t['name'], term, subjects)
        db.session.commit()


def _add_group_terms(graph, top_group, parent, vocab):
    for group in graph.objects(subject=URIRef(top_group), predicate=SKOS.term('member')):
        for concept in graph.objects(subject=group, predicate=SKOS.term('member')):
            pref, label = graph.preferredLabel(subject=concept, lang='es')[0]
            print('---->>', concept, label)
            term = Term()
            term.identifier = str(concept)
            term.description = str(label)
            term.parent_id = parent.id
            term.vocabulary_id = vocab.identifier
            db.session.add(term)

def init_indexes():

    indexes = Vocabulary()
    indexes.identifier = IrokoVocabularyIdentifiers.INDEXES.value
    indexes.human_name = 'Indices, Bases de Datos'
    db.session.add(indexes)
    db.session.commit()

    work_dir = current_app.config['HARVESTER_SECONDARY_DIRECTORY']
    miar_harvester = MiarHarvester(work_dir)
    miar_harvester.syncronize_miar_databases()

def delete_all_vocabs():
    ts = TermSources.query.all()
    for t in ts:
        db.session.delete(t)
    db.session.commit()

    s = Vocabulary.query.all()
    for so in s:
        db.session.delete(so)
    db.session.commit()



