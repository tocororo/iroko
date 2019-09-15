# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Functions for searching ES and returning the results."""

from __future__ import absolute_import, division, print_function

import os

import json
from flask import current_app

from invenio_db import db
from ..taxonomy.models import Vocabulary, Term

def init_taxonomy():
    """Init taxonomy"""
    delete_all_vocabs()
#     tax_path = '../../data/taxonomy.json' .
    path = current_app.config['INIT_TAXONOMY_JSON_PATH']
    
    with open(path) as f:
        tax = json.load(f)
        institutions = Vocabulary()
        institutions.name = 'institutions'
        db.session.add(institutions)

        subjects = Vocabulary()
        subjects.name = 'subjects'
        db.session.add(subjects)

        provinces = Vocabulary()
        provinces.name = 'provinces'
        db.session.add(provinces)
        
        data_bases = Vocabulary()
        data_bases.name = 'data_bases'
        db.session.add(data_bases)

        grupo_mes = Vocabulary()
        grupo_mes.name = 'grupo_mes'
        db.session.add(grupo_mes)

        licences = Vocabulary()
        licences.name = 'licences'
        db.session.add(licences)
        
        
        db.session.commit()
        init_vocabulary(tax, institutions)
        init_vocabulary(tax, subjects)
        init_vocabulary(tax, provinces)
        init_vocabulary(tax, data_bases)
        init_vocabulary(tax, grupo_mes)
        init_vocabulary(tax, licences)

        # db.session.commit()

def init_vocabulary(tax, vocab):
    """init a vocabulary"""

    # add all parents
    for k, term in tax[vocab.name].items():
        nterm = Term()
        nterm.name = term['name']
        nterm.vocabulary_id = vocab.id
        if term['parents'][0] != '0':
            if tax[vocab.name][term['parents'][0]]:
                parent_name = tax[vocab.name][term['parents'][0]]['name']
                parent = Term.query.filter_by(name=parent_name).first()
                nterm.parent_id = parent.id
        db.session.add(nterm)
        db.session.commit()
            
def delete_all_vocabs():
    s = Vocabulary.query.all()
    for so in s:
        db.session.delete(so)
    db.session.commit()
    


