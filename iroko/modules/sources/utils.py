from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request, json

from iroko.modules.sources.models import Sources, TermSources
from iroko.modules.taxonomy.models import Term
from iroko.modules.sources.marshmallow import sources_schema, source_schema


def get_sources_by_terms(tids)
    """sources by a list of terms"""
    termsources = TermSources.query.filter(TermSources.term_id in tids).group_by(TermSources.sources_id).all()

    result[]
    for ts in termsources:
        