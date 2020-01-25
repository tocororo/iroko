
"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request
from iroko.utils import iroko_json_response, IrokoResponseStatus
from iroko.sources.journals.marshmallow import journal_schema, journal_schema_many
from iroko.sources.models import Source, SourceType, SourceStatus, TermSources
from iroko.sources.utils import _load_terms_tree
from iroko.sources.journals.utils import _filter_data_args, _filter_extra_args
from iroko.sources.marshmallow import source_schema, source_schema_many




api_blueprint = Blueprint(
    'iroko_api_sources_journals',
    __name__,
    url_prefix='/source'
)


@api_blueprint.route('/journals')
def get_journals():
    """List all journals with filters in parameters"""
    # TODO: document this!!!
    # TODO: esto se puede hacer mas eficientemente...

    and_op = True if request.args.get('op') and request.args.get('op') == 'and' else False

    count = int(request.args.get('count')) if request.args.get('count') else 10
    page = int(request.args.get('page')) if request.args.get('page') else 0

    limit = count
    offset = count*page

    tids = request.args.get('terms')
    terms = []
    if tids:
        tids= tids.split(',')
        term_op = tids[0]
        if tids[0].lower() == 'and' or tids[0].lower() == 'or':
            del tids[0]
        terms = tids

    extra_args = {
        'source_type' : SourceType.JOURNAL.value,
        'source_status': SourceStatus.APPROVED.value
    }
    # str(request.args.get('source_status'))

    data_args = {
        'title' : str(request.args.get('title')),
        'description': str(request.args.get('description')),
        'url': str(request.args.get('url')),
        'issn': str(request.args.get('issn')),
        'rnps': str(request.args.get('rnps')),
        'year_start': str(request.args.get('year_start')),
        'year_end': str(request.args.get('year_end'))
    }

    result = []
    all_terms = _load_terms_tree(terms)
    filter_terms = len(all_terms) > 0
    if filter_terms:
        sources = TermSources.query.filter(TermSources.term_id.in_(all_terms)).all()
    else:
        sources = Source.query.order_by('name').all()

    for item in sources:
        source = item.source if filter_terms else item
        in_data = _filter_data_args(source, data_args, and_op)
        in_extra = _filter_extra_args(source, extra_args, and_op)
        if and_op and in_data and in_extra:
            result.append(source)
        else:
            if in_data or in_extra:
                result.append(source)

    if result is not None:
        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': journal_schema_many.dump(result[offset:offset+limit]),\
                         'count': len(result)})
    return iroko_json_response(IrokoResponseStatus.NOT_FOUND, 'Sources not found', None, {'count': 0})


@api_blueprint.route('/journal/<uuid>')
def get_journal_by_uuid(uuid):
    """Get a journal by UUID"""
    try: 
        source = Source.query.filter_by(uuid=uuid, source_type=SourceType.JOURNAL)
        if not source:
            raise Exception('Source not found')

        return iroko_json_response(IrokoResponseStatus.SUCCESS, \
                        'ok','sources', \
                        {'data': source_schema.dump(source), 'count': 1})

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)