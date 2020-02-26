"""
Helper function to several task related to Sources, sources types,
 sources fields, etc..
"""

from invenio_db import db
from iroko.sources.models import Source, TermSources, SourceStatus, SourceType, SourceVersion
from iroko.taxonomy.models import Term
from iroko.sources.marshmallow.base import TermSourcesSchema

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
    #TODO validar UUID
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


def sync_term_source_with_data(source:Source):
    """The model TermSources map the relations of Source with any term. In source.data[terms] are all the term ids related to the source, this is done this way to simplify the consumer apps and version handling. This function use source.data to sync term-source relations, meaning that new relations in source.data will be included in TermSource table, and relations in TermSource not present in source.data will be removed."""
    # print("not implemented")

    TermSources.query.filter_by(sources_id=source.id).delete()
    print("delete")
    db.session.commit()
    print("commit")
    data = dict(source.data)

    if "term_sources" in data:
        # new_terms = []
        for ts in data["term_sources"]:
            print(ts)
            t=Term.query.filter_by(id=ts['term_id']).first()
            if t is not None:
                new_ts = TermSources()
                print("new")
                new_ts.sources_id = source.id
                new_ts.term_id = t.id
                new_ts.data = ts['data']
                db.session.add(new_ts)
                # new_terms.append(new_ts)
                print("append ")
        # schema = TermSourcesSchema(many=True)
        # data["term_sources"] = schema.dump(new_terms)
        # source.data = data
        db.session.commit()


