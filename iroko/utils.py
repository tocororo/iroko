from __future__ import absolute_import, print_function

import enum
from flask import jsonify
from flask import g, request
# from invenio_app import babel

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


# @babel.localeselector
# def get_locale():
#     # if a user is logged in, use the locale from the user settings
#     user = getattr(g, 'user', None)
#     if user is not None:
#         return user.locale
#     # otherwise try to guess the language from the user accept
#     # header the browser transmits.  We support de/fr/en in this
#     # example.  The best match wins.
#     return request.accept_languages.best_match(['de', 'fr', 'en'])


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