

from sqlalchemy import and_, or_, not_
from iroko.sources.models import Source, TermSources
from iroko.taxonomy.models import Term
from iroko.sources.marshmallow import sources_schema, sources_schema_full, SourceSchema
from invenio_db import db

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
    """aux func"""
    if term.children:
        children = []
        for child in term.children:
            children.append(child.id)
            _load_term_children_id(child)
        return children

def _filter_data_args(source:Source, data, and_op):
    """ aux func.
    esto es ineficiente... pero es lo que hay.. por el momento.. 
    solo debe usarse para la lista de revistas que no pasa de 300
    TODO: optimizar..."""
    
    if source.data is None:
        return True
    if _no_params(data):
        return True

    title = data['title'].lower() in str(source.name).lower()
    description = data['description'] in source.data['description'] \
        if 'description' in source.data else False
    url = data['url'] in source.data['url'] if 'url' in source.data else False

    issn = False
    if 'issn' in source.data:
        issn_p = data['issn'].lower() in source.data['issn']['p'].lower() if 'p' in source.data['issn'] else False
        issn_e = data['issn'].lower() in source.data['issn']['e'].lower() if 'e' in source.data['issn']else False
        issn_l = data['issn'].lower() in source.data['issn']['l'].lower() if 'l' in source.data['issn']else False
        issn = issn_p or issn_e or issn_l

    rnps = data['rnps'].lower() in source.data['rnps'].lower() if 'rnps' in source.data else False
    year_start = data['year_start'].lower() in source.data['year_start'].lower() if 'year_start' in source.data else False
    year_end = data['year_end'].lower() in source.data['year_end'].lower() if 'year_end' in source.data else False

    if and_op:
        return title and description and url and issn and rnps and year_start and year_end
    else: 
        return title or description or url or issn or rnps or year_start or year_end

def _filter_repo_args(source:Source, repo_args, and_op):
    """ aux func.
    esto es ineficiente...lo mismo que _filter_data_args"""

    harvest_type = source.repo_harvest_type == repo_args['harvest_type']
    harvest_status = source.repo_status == repo_args['harvest_status']
    has_harvest_endpoint = source.repo_harvest_endpoint is not None

    if and_op:
        return harvest_type and harvest_status and harvest_status
    else: 
        return harvest_type or harvest_status or harvest_status


class Sources:
    """API for manipulation of Sources
    Considering SourceVersion: meanining this class use Source and SourceVersion model. 
    """

    # Listar todas las fuentes dado un status...
    # Listar una fuente con sus versiones
    # saber si de una version con un status determinado tiene una nueva version que no es "current"

    @classmethod
    def get_sources(cls, and_op, terms, data_args, repo_args):
        """return Source array"""

        result = []
        all_terms = _load_terms_tree(terms)
        filter_terms = len(all_terms) > 0
        if filter_terms:
            sources = TermSources.query.filter(TermSources.term_id.in_(all_terms)).all()
        else:
            sources = Source.query.order_by('name').all()

        # TODO: esto se puede hacer mas eficientemente...
        for item in sources:
            source = item.source if filter_terms else item
            in_data = _filter_data_args(source, data_args, and_op)
            in_repo = _filter_repo_args(source, repo_args, and_op)
            if and_op and in_data and in_repo:
                result.append(source)
            else: 
                if in_data or in_repo:
                    result.append(source)
        return result

    @classmethod
    def get_source_by_id(cls, id=None, uuid= None):
        if id is not None:
            return Source.query.filter_by(id=id).first()
        if uuid is not None:
            return Source.query.filter_by(uuid=uuid).first()

    @classmethod
    def count_sources(cls):
        return Source.query.count()

