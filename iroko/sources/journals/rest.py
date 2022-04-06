#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, request

from iroko.sources.journals.utils import _filter_data_args, _filter_extra_args
from iroko.sources.marshmallow.source import source_schema, source_schema_many
from iroko.sources.models import Source, SourceRawData, SourceStatus, SourceType, TermSources
from iroko.sources.utils import _load_terms_tree
from iroko.utils import IrokoResponseStatus, iroko_json_response

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

    count = int(request.args.get('size')) if request.args.get('size') else 10
    page = int(request.args.get('page')) if request.args.get('page') else 1

    if page < 1:
        page = 1
    offset = count * (page - 1)
    limit = offset + count

    tids = request.args.get('terms')
    terms = []
    if tids:
        tids = tids.split(',')
        term_op = tids[0]
        if tids[0].lower() == 'and' or tids[0].lower() == 'or':
            del tids[0]
        terms = tids

    extra_args = {
        'source_type': SourceType.JOURNAL.value,
        'source_status': SourceStatus.APPROVED.value
        }
    # str(request.args.get('source_status'))

    data_args = {
        'title': str(request.args.get('title')),
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
                # print(source.data)
                result.append(source)
    # print("---- - - - - - - -  -----------")
    if result is not None:
        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            'ok', 'sources', \
            {
                'data': source_schema_many.dump(result[offset:limit]), \
                'count': len(result)
                }
            )
    return iroko_json_response(
        IrokoResponseStatus.NOT_FOUND, 'Sources not found', None, {'count': 0}
        )


@api_blueprint.route('/journal/<uuid>')
def get_journal_by_uuid(uuid):
    """Get a journal by UUID"""
    try:
        source = Source.query.filter_by(uuid=uuid, source_type=SourceType.JOURNAL)
        if not source:
            raise Exception('Source not found')

        return iroko_json_response(
            IrokoResponseStatus.SUCCESS, \
            'ok', 'sources', \
            {'data': source_schema.dump(source), 'count': 1}
            )

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)


@api_blueprint.route('/journal/issn/<issn>')
def get_journal_by_issn(issn):
    """Get a journal by UUID"""
    # print('def get_journal_by_issn(issn):')
    try:
        issn_db = SourceRawData.query.filter_by(identifier=issn).first()
        if not issn_db:
            return iroko_json_response(
                IrokoResponseStatus.NOT_FOUND,
                "ISSN {0} not found on Cuban ISSNs list".format(issn), None, None
                )
            # raise Exception("ISSN {0} not found on Cuban ISSNs list".format(issn))
        issns_with_info = issn_db.data

        if not "@graph" in issns_with_info.keys():
            raise Exception("Wrong json format for ISSN: {0}".format(issn))

        for item in issns_with_info["@graph"]:
            if item['@id'] == 'resource/ISSN/' + issn + '#KeyTitle':
                return iroko_json_response(
                    IrokoResponseStatus.SUCCESS,
                    "ok", "issn_org",
                    {"issn": issn, "title": item["value"]}
                    )

            # if "issn" in item.keys() and "name" in item.keys():
            #     return iroko_json_response(IrokoResponseStatus.SUCCESS,
            #     "ok", "ISSN validation",
            #     {"issn":issn, "name":item["name"]})

        raise Exception("Internal Error: Name not found on the ISSN info")

    except Exception as e:
        return iroko_json_response(IrokoResponseStatus.ERROR, str(e), None, None)
