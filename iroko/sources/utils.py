#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""
Helper function to several task related to Sources, sources types,
 sources fields, etc..
"""


from iroko.vocabularies.models import Term


def _load_terms_tree(terms):
    """aux func"""
    temp_terms = []
    for par_term in terms:
        if str(par_term).isdigit():
            temp_terms += [par_term]
            aux = Term.query.filter_by(id=par_term).first()
            tchildren = _load_term_children_id(aux)
            if tchildren:
                temp_terms += tchildren
    return set(temp_terms)


def _load_terms_tree_by_uuid(terms):
    """aux func"""
    # TODO validar UUID
    temp_terms = []
    for uuid in terms:
        temp_terms += [str(uuid)]
        aux = Term.query.filter_by(uuid=uuid).first()
        tchildren = _load_term_children_uuid(aux)
        if tchildren:
            temp_terms += tchildren
    return temp_terms


def _load_term_children_id(term):
    """aux func to load Term tree"""
    if term.children:
        children = []
        for child in term.children:
            children.append(child.id)
            _load_term_children_id(child)
        return children


def _load_term_children_uuid(term):
    """aux func to load Term tree"""
    if term.children:
        children = []
        for child in term.children:
            children.append(str(child.uuid))
            _load_term_children_id(child)
        return children
