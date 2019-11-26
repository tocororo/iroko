"""
Helper function to several task related to Sources, sources types,
 sources fields, etc..
"""

from invenio_db import db
from iroko.sources.models import Source, TermSources, SourceStatus, SourceType, SourceVersion
from iroko.taxonomy.models import Term


def _no_params(param_data):
    """aux func"""
    return param_data['title'] == 'None' and \
        param_data['description'] == 'None' and \
        param_data['url'] == 'None' and \
        param_data['issn'] == 'None' and \
        param_data['rnps'] == 'None' and \
        param_data['year_start'] == 'None' and \
        param_data['year_end'] == 'None'


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


def _load_term_children_id(term):
    """aux func to load Term tree"""
    if term.children:
        children = []
        for child in term.children:
            children.append(child.id)
            _load_term_children_id(child)
        return children


def _filter_data_args(source:Source, data_args, and_op):
    """ aux func."""

    # esto es ineficiente... pero es lo que hay.. por el momento..
    # solo debe usarse para la lista de revistas que no pasa de 300
    # TODO: como optimizar...?

    if source.data is None:
        return True
    if _no_params(data_args):
        return True

    title = data_args['title'].lower() in str(source.name).lower()
    description = data_args['description'] in source.data['description'] \
        if 'description' in source.data else False
    url = data_args['url'] in source.data['url'] if 'url' in source.data else False

    issn = False
    if 'issn' in source.data:
        issn_p = data_args['issn'].lower() in source.data['issn']['p'].lower() if 'p' in source.data['issn'] else False
        issn_e = data_args['issn'].lower() in source.data['issn']['e'].lower() if 'e' in source.data['issn']else False
        issn_l = data_args['issn'].lower() in source.data['issn']['l'].lower() if 'l' in source.data['issn']else False
        issn = issn_p or issn_e or issn_l

    rnps = data_args['rnps'].lower() in source.data['rnps'].lower() if 'rnps' in source.data else False
    year_start = data_args['year_start'].lower() in source.data['year_start'].lower() if 'year_start' in source.data else False
    year_end = data_args['year_end'].lower() in source.data['year_end'].lower() if 'year_end' in source.data else False

    if and_op:
        return title and description and url and issn and rnps and year_start and year_end
    else:
        return title or description or url or issn or rnps or year_start or year_end


def _filter_repo_args(source:Source, repo_args, and_op):
    """ aux func.
    esto es ineficiente...lo mismo que _filter_data_args"""

    if repo_args is None:
        return True

    harvest_type = source.repo_harvest_type == repo_args['harvest_type']
    harvest_status = source.repo_status == repo_args['harvest_status']
    has_harvest_endpoint = source.repo_harvest_endpoint is not None

    if and_op:
        return harvest_type and harvest_status and harvest_status
    else:
        return harvest_type or harvest_status or harvest_status


def issn_is_in_data(data, issn:str, equal: bool):
    """Check if issn param is in any of the regular data ISSNs (print, electronic, link)
    if equal is True check exactly the value of issn param
    normally data have this structure
    {
        ...
        issn:{
            p:"XXXX-YYYY",
            e:"XXXX-YYYY",
            l:"XXXX-YYYY"
        }
        ...
    }

    param: data: data JSON of journals
    param: issn: string to compare
    param: equal: bool
    :rtype: bool
    """

    if issn and 'issn' in data:
        if equal:
            issn_p = issn.lower() == data['issn']['p'].lower() if 'p' in data['issn'] else False
            issn_e = issn.lower() == data['issn']['e'].lower() if 'e' in data['issn'] else False
            issn_l = issn.lower() == data['issn']['l'].lower() if 'l' in data['issn'] else False
        else:
            issn_p = issn.lower() in data['issn']['p'].lower() if 'p' in data['issn'] else False
            issn_e = issn.lower() in data['issn']['e'].lower() if 'e' in data['issn'] else False
            issn_l = issn.lower() in data['issn']['l'].lower() if 'l' in data['issn'] else False
        return issn_p or issn_e or issn_l
    return False


def field_is_in_data(data, field_name:str, field_value:str, equal:bool):
    """Check if field_value is in data[field_name]
    if equal is True,field_value == data[field_name]

    always check before if data[field_name] exist

    """
    result = False
    if field_value:
        if equal:
            result = field_value.lower() == data[field_name].lower() if field_name in data else False
        else:
            result = field_value.lower() in data[field_name].lower() if field_name in data else False
    return result


def sync_term_source_with_data(source:Source):
    """The model TermSources map the relations of Source with any term. In source.data[terms] are all the term ids related to the source, this is done this way to simplify the consumer apps and version handling. This function use source.data to sync term-source relations, meaning that new relations in source.data will be included in TermSource table, and relations in TermSource not present in source.data will be removed."""
    # print("not implemented")

    db.session.query(TermSources).filter(sources_id=source.id).delete()
    db.session.commit()

    data = dict(source.data)

    if "terms" in data:
        new_terms = []
        for tid in data["terms"]:
            t=Term.query.filter_by(id=tid['id']).first()
            if t is not None:
                ts = TermSources()
                ts.sources_id = source.id
                ts.term_id = tid['id']
                ts.data = tid['data']
                db.session.add(ts)
                new_terms.append(tid)
        data["terms"] = new_terms
        source.data = data
        db.session.commit()


