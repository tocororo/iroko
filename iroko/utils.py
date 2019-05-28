from __future__ import absolute_import, print_function

import enum
from flask import jsonify

# def get_sources_by_terms(tids):
#     """sources by a list of terms"""
#     termsources = TermSources.query.filter(TermSources.term_id in tids).group_by(TermSources.sources_id).all()

#     result[]
#     for ts in termsources:
class IrokoResponseStatus(enum.Enum):
    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"
    NOT_FOUND = "not found"


def iroko_json_response(status: IrokoResponseStatus, message, data_type, data):
    """recibe la respuesta de marshmallow.dump(model)"""

    return jsonify({
        'status':status.value,
        'message': message,
        'data': {
            data_type: data
        }
    })


def get_identifier_schema(pid):
    identifiers_schemas = [
        "ark",
        "arxiv",
        "doi",
        "bibcode",
        "ean8",
        "ean13",
        "eissn",
        "handle",
        "isbn",
        "issn",
        "istc",
        "lissn",
        "lsid",
        "pmid",
        "pmcid",
        "purl",
        "upc",
        "url",
        "urn",
        "orcid",
        "gnd",
        "ads"
    ]
    for schema in identifiers_schemas:
        if schema in pid:
            return schema
    if 'http' in pid or 'https' in pid:
        return 'url'
    return None