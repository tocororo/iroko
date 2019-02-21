# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 UPR.
#
# iroko is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration for iroko.

You overwrite and set instance-specific configuration by either:

- Configuration file: ``<virtualenv prefix>/var/instance/invenio.cfg``
- Environment variables: ``APP_<variable name>``
"""

from __future__ import absolute_import, print_function

import os

from datetime import timedelta
from invenio_records_rest.utils import allow_all

def _(x):
    """Identity function used to trigger string extraction."""
    return x

IP_ELASTIC = '10.2.83.93'
IP_POSGRE = '10.80.4.151'
IP_RABBIT = '10.80.4.250'
IP_REDIS = '10.80.4.109'


ACCOUNTS_SESSION_REDIS_URL='redis://'+IP_REDIS+':6379/1'
BROKER_URL='amqp://iroko:iroko@'+IP_RABBIT+':5672/'
CACHE_REDIS_URL='redis://'+IP_REDIS+':6379/0'
CACHE_TYPE='redis'
CELERY_BROKER_URL='amqp://iroko:iroko@'+IP_RABBIT+':5672/'
CELERY_RESULT_BACKEND='redis://'+IP_REDIS+':6379/2'

SECRET_KEY='iroko_secret_key'
SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://iroko:iroko@'+IP_POSGRE+'/iroko'
WSGI_PROXIES=2
RATELIMIT_STORAGE_URL='redis://'+IP_REDIS+':6379/3'


# SEARCH_ELASTIC_HOSTS='["http://"]'
params = dict(
#    http_auth=('admin', 'malayibiri'),
)
SEARCH_ELASTIC_HOSTS = [
    dict(host=IP_ELASTIC, **params)
]



# Rate limiting
# =============
#: Storage for ratelimiter.
RATELIMIT_STORAGE_URL = 'redis://'+IP_REDIS+':6379/3'

# I18N
# ====
#: Default language
BABEL_DEFAULT_LANGUAGE = 'en'
#: Default time zone
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
#: Other supported languages (do not include the default language in list).
I18N_LANGUAGES = [
    # ('fr', _('French'))
]

# Base templates
# ==============
#: Global base template.
BASE_TEMPLATE = 'invenio_theme/page.html'
#: Cover page base template (used for e.g. login/sign-up).
COVER_TEMPLATE = 'invenio_theme/page_cover.html'
#: Footer base template.
FOOTER_TEMPLATE = 'invenio_theme/footer.html'
#: Header base template.
HEADER_TEMPLATE = 'invenio_theme/header.html'
#: Settings base template.
SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'

# Theme configuration
# ===================
#: Site name
THEME_SITENAME = _('iroko')
#: Use default frontpage.
THEME_FRONTPAGE = True
#: Frontpage title.
THEME_FRONTPAGE_TITLE = _('iroko')
#: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'iroko/frontpage.html'

# Email configuration
# ===================
#: Email address for support.
SUPPORT_EMAIL = "info@inveniosoftware.org"
#: Disable email sending by default.
MAIL_SUPPRESS_SEND = True

# Assets
# ======
#: Static files collection method (defaults to copying files).
COLLECT_STORAGE = 'flask_collect.storage.file'

# Accounts
# ========
#: Email address used as sender of account registration emails.
SECURITY_EMAIL_SENDER = SUPPORT_EMAIL
#: Email subject for account registration emails.
SECURITY_EMAIL_SUBJECT_REGISTER = _(
    "Welcome to iroko!")
#: Redis session storage URL.
ACCOUNTS_SESSION_REDIS_URL = 'redis://'+IP_REDIS+':6379/1'

# Celery configuration
# ====================

BROKER_URL = 'amqp://iroko:iroko@'+IP_RABBIT+':5672/'
#: URL of message broker for Celery (default is RabbitMQ).
CELERY_BROKER_URL = 'amqp://iroko:iroko@'+IP_RABBIT+':5672/'
#: URL of backend for result storage (default is Redis).
CELERY_RESULT_BACKEND = 'redis://'+IP_REDIS+':6379/2'
#: Scheduled tasks configuration (aka cronjobs).
CELERY_BEAT_SCHEDULE = {
    'indexer': {
        'task': 'invenio_indexer.tasks.process_bulk_queue',
        'schedule': timedelta(minutes=5),
    },
    'accounts': {
        'task': 'invenio_accounts.tasks.clean_session_table',
        'schedule': timedelta(minutes=60),
    },
}

# Database
# ========
#: Database URI including user and password
#SQLALCHEMY_DATABASE_URI = \
#    'postgresql+psycopg2://iroko:iroko@'+IP_POSGRE+'/iroko'

# JSONSchemas
# ===========
#: Hostname used in URLs for local JSONSchemas.
JSONSCHEMAS_HOST = 'iroko.upr.edu.cu'

# Flask configuration
# ===================
# See details on
# http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values

#: Secret key - each installation (dev, production, ...) needs a separate key.
#: It should be changed before deploying.
SECRET_KEY = 'CHANGE_ME'
#: Max upload size for form data via application/mulitpart-formdata.
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MiB
#: Sets cookie with the secure flag by default
SESSION_COOKIE_SECURE = True
#: Since HAProxy and Nginx route all requests no matter the host header
#: provided, the allowed hosts variable is set to localhost. In production it
#: should be set to the correct host and it is strongly recommended to only
#: route correct hosts to the application.
APP_ALLOWED_HOSTS = ['localhost', '127.0.0.1','10.80.4.34']

# OAI-PMH
# =======
OAISERVER_ID_PREFIX = 'oai:iroko.upr.edu.cu:'

# Debug
# =====
# Flask-DebugToolbar is by default enabled when the application is running in
# debug mode. More configuration options are available at
# https://flask-debugtoolbar.readthedocs.io/en/latest/#configuration

#: Switches off incept of redirects by Flask-DebugToolbar.
DEBUG_TB_INTERCEPT_REDIRECTS = False

FLASK_ADMIN_SWATCH = 'default'


###############################################################################
# JSON Schemas
###############################################################################

JSONSCHEMAS_ENDPOINT = '/schemas'
JSONSCHEMAS_HOST = os.environ.get('JSONSCHEMAS_HOST', 'localhost:5000')
JSONSCHEMAS_URL_SCHEME = 'https'





#: Records REST API endpoints.
# RECORDS_API = '/api/records/{pid_value}'
# RECORDS_REST_ENDPOINTS = dict(
#     recid=dict(
#         pid_type='recid',
#         pid_minter='iroko_record_minter',
#         pid_fetcher='iroko_record_fetcher',
#         list_route='/records/',
#         item_route='/records/<{0}:pid_value>'.format(
#             'pid(recid,record_class="iroko.modules.records.api:IrokoRecord")'
#         ),
#         search_index='records',
#         record_class='iroko.modules.records.api:IrokoRecord',
#         search_type=['record-v1.0.0'],
#         search_factory_imp='iroko.modules.records.query.search_factory',
#         record_serializers={
#             'application/json': (
#                 'iroko.modules.records.serializers.legacyjson_v1_response'),
#             'application/vnd.iroko.v1+json': (
#                 'iroko.modules.records.serializers.json_v1_response'),
#             'application/ld+json': (
#                 'iroko.modules.records.serializers.schemaorg_jsonld_v1_response'),
#             'application/marcxml+xml': (
#                 'iroko.modules.records.serializers.marcxml_v1_response'),
#             'application/x-bibtex': (
#                 'iroko.modules.records.serializers.bibtex_v1_response'),
#             'application/x-datacite+xml': (
#                 'iroko.modules.records.serializers.datacite_v31_response'),
#             'application/x-datacite-v41+xml': (
#                 'iroko.modules.records.serializers.datacite_v41_response'),
#             'application/x-dc+xml': (
#                 'iroko.modules.records.serializers.dc_v1_response'),
#             'application/vnd.citationstyles.csl+json': (
#                 'iroko.modules.records.serializers.csl_v1_response'),
#             'text/x-bibliography': (
#                 'iroko.modules.records.serializers.citeproc_v1_response'),
#         },
#         search_serializers={
#             'application/json': (
#                 'iroko.modules.records.serializers:legacyjson_v1_search'),
#             'application/vnd.iroko.v1+json': (
#                 'iroko.modules.records.serializers:json_v1_search'),
#             'application/marcxml+xml': (
#                 'iroko.modules.records.serializers.marcxml_v1_search'),
#             'application/x-bibtex': (
#                 'iroko.modules.records.serializers:bibtex_v1_search'),
#             'application/x-datacite+xml': (
#                 'iroko.modules.records.serializers.datacite_v31_search'),
#             'application/x-dc+xml': (
#                 'iroko.modules.records.serializers.dc_v1_search'),
#         },
#         default_media_type='application/vnd.iroko.v1+json',
#         read_permission_factory_imp=allow_all,
#     ),
# )