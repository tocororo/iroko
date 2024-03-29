#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, print_function

import enum
import re
from threading import Thread
from uuid import UUID

from flask import current_app, jsonify, render_template, request
from flask_mail import Message
from invenio_accounts.models import User
from invenio_i18n.selectors import get_locale

#     result[]
#     for ts in termsources:
# from iroko.organizations.api import OrganizationRecord


# def get_sources_by_terms(tids):
#     """sources by a list of terms"""
#     termsources = TermSources.query.filter(TermSources.term_id in tids).group_by(
#     TermSources.sources_id).all()


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

    return jsonify(
        {
            'status': status.value,
            'message': message,
            'data': {
                data_type: data
                }
            }
        )


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
    return re.sub('\W+|^(?=\d)', '_', value.lower())


def send_async_email(app, msg):
    with app.app_context():
        app.extensions['mail'].send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg) #esto lo mando pero no asincronamente
    Thread(target=send_async_email, args=(current_app, msg)).start()


def send_contact_email(name, email, user_message):
    language = get_locale().upper()
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    send_email(
        'message from sceiba',
        sender=current_app.config['SECURITY_EMAIL_SENDER'],
        # recipients=current_app.config['ADMINS'],
        recipients=email,
        text_body=render_template(
            'iroko_theme/email/contact_email.txt', name=name, email=email,
            user_message=user_message, language=language, ip=client_ip
            ),
        html_body=render_template(
            'iroko_theme/email/contact_email.html', name=name, email=email,
            user_message=user_message, language=language, ip=client_ip
            )
        )


def get_default_user():
    user = User.query.filter_by(email='rafael.martinez@upr.edu.cu').first()
    if not user:
        user = User.query.filter_by(email='sceiba.cu@gmail.com').first()
    return user


class CuorHelper:
    # TODO: investigar como hacer esto mas eficientemente, con redis quizas
    org_simple_cache = dict()

    @classmethod
    def query_cuor_by_label(cls, text, country='', state='', types=''):
        """get the fist name found in labels.label"""
        try:
            # search = OrganizationRecord.get_search(text, country, state, types)
            # hit = search.scan()[0]
            # pid, org = OrganizationRecord.get_org_by_pid(hit.id)
            return None

            # api_endpoint = current_app.config['CUOR_API_ENDPOINT']
            # session = requests.Session()
            # url = api_endpoint + '?q=labels.label:' + text
            # if country != '':
            #     url += '&country=' + country
            # if state != '':
            #     url += '&state=' + state
            # if types != '':
            #     url += '&types=' + types
            # response = session.get(url, verify=False)
            # result = json.loads(response.text)
            # if 'hits' in result and 'total' in result['hits'] and result['hits']['total'] > 0:
            #     return result['hits']['hits'][0]
        except Exception:
            return None


def remove_nulls(d):
    return {k: v for k, v in d.items() if v is not None}


def _assing_if_exist(data, record, field):
    if field in record:
        data[field] = record[field]
