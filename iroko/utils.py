from __future__ import absolute_import, print_function

import enum
# from invenio_app import babel
import re
from uuid import UUID

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


class IrokoVocabularyIdentifiers(enum.Enum):
    COUNTRIES = 'COUNTRIES'
    CUBAN_PROVINCES = 'CUBAN_PROVINCES',
    LICENCES = 'LICENCES',
    CUBAN_INTITUTIONS = 'CUBAN_INTITUTIONS',
    EXTRA_INSTITUTIONS = 'EXTRA_INSTITUTIONS',
    SUBJECTS = 'SUBJECTS',
    INDEXES = 'INDEXES',
    INDEXES_CLASIFICATION = 'INDEXES_CLASIFICATION',
    RECOD_SETS = 'RECOD_SETS',
    RECORD_TYPES = 'RECORD_TYPES',



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

identifiers_schemas = [
        "ark",
        "arxiv",
        "doi",
        "bibcode",
        "ean8",
        "ean13",
        "handle",
        "isbn",
        "pissn",
        "lissn",
        "eissn",
        "istc",
        "lsid",
        "pmid",
        "pmcid",
        "purl",
        "upc",
        "url",
        "urn",
        "orcid",
        "gnd",
        "ads",
        "oai",
        "prnps",
        "ernps",
        "oaiurl",
        "grid",
        "wikidata",
        "ror",
        "isni",
        "orgref",
        "reup"
    ]

def get_identifier_schema(pid):

    for schema in identifiers_schemas:
        if schema in pid:
            return schema
    if 'http' in pid or 'https' in pid:
        return 'url'
    return None


def validate_uuid4(uuid_string):

    """
    Validate that a UUID string is in
    fact a valid uuid4.
    Happily, the uuid module does the actual
    checking for us.
    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    """

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    # If the uuid_string is a valid hex code,
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a
    # valid uuid4. This is bad for validation purposes.

    return val.hex == uuid_string or str(val) == uuid_string


def validate_integer(int_string):
    try:
        aux = int(int_string)
        return True
    except ValueError as e:
        return False

def string_as_identifier(value: str):
    return re.sub('\W+|^(?=\d)','_', value.lower())
