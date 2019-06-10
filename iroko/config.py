# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 UPR.
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Default configuration for iroko.

You overwrite and set instance-specific configuration by either:

- Configuration file: ``<virtualenv prefix>/var/instance/invenio.cfg``
- Environment variables: ``APP_<variable name>``
"""

from __future__ import absolute_import, print_function
import os
from datetime import timedelta

from .dev_ip import IP_ELASTIC, IP_POSGRE, IP_RABBIT, IP_REDIS, APP_ALLOWED_HOSTS, IROKO_HOST

from invenio_indexer.api import RecordIndexer
from invenio_records_rest.facets import terms_filter, range_filter
from invenio_records_rest.utils import allow_all, check_elasticsearch
from invenio_search import RecordsSearch
from flask_babelex import lazy_gettext as _

from invenio_app.config import APP_DEFAULT_SECURE_HEADERS as INVENIO_APP_APP_DEFAULT_SECURE_HEADERS

def _(x):
    """Identity function used to trigger string extraction."""
    return x


CACHE_REDIS_URL='redis://'+IP_REDIS+':6379/0'
CACHE_TYPE='redis'




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
    ('es', _('Spanish')) ,
]


# Base templates
# ==============
REQUIREJS_CONFIG = 'js/build.js'

SASS_BIN = 'node-sass'

#: Global base template.
BASE_TEMPLATE = 'iroko_theme/page.html'
THEME_BASE_TEMPLATE = 'iroko_theme/page.html'
#: Cover page base template (used for e.g. login/sign-up).
COVER_TEMPLATE = 'iroko_theme/page_cover.html'

THEME_BODY_TEMPLATE = 'iroko_theme/body.html'

#: Header base template.
THEME_HEADER_TEMPLATE = 'iroko_theme/header.html'
#: Footer base template.
THEME_FOOTER_TEMPLATE = 'iroko_theme/footer.html'

SECURITY_LOGIN_USER_TEMPLATE = 'iroko_theme/accounts/login_user.html'

SECURITY_REGISTER_USER_TEMPLATE = 'iroko_theme/accounts/register_user.html'

THEME_SEARCHBAR = True

THEME_HEADER_LOGIN_TEMPLATE = 'iroko_theme/header_login.html'
#: Settings base template.
SETTINGS_TEMPLATE = 'iroko_theme/page_settings.html'

# Theme configuration
# ===================
#: Site name
THEME_SITENAME = _('sceiba')
#: Use default frontpage.
THEME_FRONTPAGE = False
#: Frontpage title.
THEME_FRONTPAGE_TITLE = _('sceiba')
#: Theme logo.
THEME_LOGO = 'images/sceiba-logo.png'
THEME_LOGO_ADMIN = 'images/sceiba-logo.png'
#: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'iroko_theme/frontpage.html'
THEME_JAVASCRIPT_TEMPLATE = 'iroko_theme/javascript.html'


# Search configuration
# ===================

"""Records UI for iroko."""
SEARCH_UI_SEARCH_API = '/api/records/'
"""Configure the search engine endpoint."""

SEARCH_UI_SEARCH_INDEX = 'records'
"""Name of the search index used."""

SEARCH_UI_JSTEMPLATE_RESULTS = 'templates/search_ui/results.html'
"""Result list template."""

SEARCH_UI_HEADER_TEMPLATE = 'iroko_theme/search_ui/base_header.html'

SEARCH_UI_SEARCH_TEMPLATE = 'iroko_theme/search_ui/search.html'
"""Configure the search page template."""

SEARCH_UI_JSTEMPLATE_COUNT = 'templates/search_ui/count.html'
"""Configure the count template."""

SEARCH_UI_JSTEMPLATE_ERROR = 'templates/search_ui/error.html'
"""Configure the error page template."""

SEARCH_UI_JSTEMPLATE_FACETS = 'templates/search_ui/facets.html'
"""Configure the facets template."""

SEARCH_UI_JSTEMPLATE_RANGE = 'templates/search_ui/range.html'
"""Configure the range template."""

SEARCH_UI_JSTEMPLATE_RANGE_OPTIONS = {'histogramId': '#year_hist',
                                      'selectionId': '#year_select',
                                      'name': 'years',
                                      'width': 180}
"""Configure the range template options."""

SEARCH_UI_JSTEMPLATE_LOADING = 'templates/search_ui/loading.html'
"""Configure the loading template."""

SEARCH_UI_JSTEMPLATE_PAGINATION = 'templates/search_ui/pagination.html'
"""Configure the pagination template."""

SEARCH_UI_JSTEMPLATE_SELECT_BOX = 'templates/search_ui/selectbox.html'
"""Configure the select box template."""

SEARCH_UI_JSTEMPLATE_SORT_ORDER = 'templates/search_ui/togglebutton.html'
"""Configure the toggle button template."""


# Records configuration
# ===================


RECORDS_UI_ENDPOINTS = {
    'recid': {
        'pid_type': 'irouid',
        'route': '/records/<pid_value>',
        'template': 'iroko_theme/records/record.html',
        'view_imp': 'iroko.records.views.iroko_record_view'
    },
}


RECORDS_REST_ENDPOINTS = {
    'irouid': {
        'pid_type': 'irouid',
        'pid_minter': 'irouid',
        'pid_fetcher': 'irouid',
        'default_endpoint_prefix': True,
        'search_class': RecordsSearch,
        'indexer_class': RecordIndexer,
        'search_index': 'records',
        'search_type': None,
        'record_serializers': {
            'application/json': ('iroko.records.serializers'
                                 ':json_v1_response'),
        },
        'search_serializers': {
            'application/json': ('iroko.records.serializers'
                                 ':json_v1_search'),
        },
        'record_loaders': {
            'application/json': ('iroko.records.loaders'
                                 ':json_v1'),
        },
        'list_route': '/records/',
        'item_route': '/records/<pid(irouid):pid_value>',
        'default_media_type': 'application/json',
        'max_result_window': 10000,
        'error_handlers': { },
        'create_permission_factory_imp': allow_all,
        'read_permission_factory_imp': check_elasticsearch,
        'update_permission_factory_imp': allow_all,
        'delete_permission_factory_imp': allow_all,
        'list_permission_factory_imp': allow_all,
        'suggesters': {
            'title': {
                'completion': {
                    'field': 'suggest_title'
                }
            }
        }
    },
}

"""REST API for iroko."""

PIDSTORE_RECID_FIELD = 'id'

IROKO_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""


RECORDS_REST_FACETS = {
    'records':{
        "filters": {
            'keywords': terms_filter('keywords'),
            'creators': terms_filter('creators.name'),
            # 'spec': terms_filter('spec.name'),
            'sources': terms_filter('source.name')
        },
        'aggs':{
            'keywords':{
                'terms':{
                    'field': 'keywords',
                    'size' : 5
                },
                "meta": {
                    "title": "Keywords",
                    "order": 3,
                }
            },
            'creators':{
                'terms':{
                    'field': 'creators.name',
                    'size' : 5
                },
                "meta": {
                    "title":  "Authors",
                    "order": 2,
                }
            },
            # 'spec':{
            #     'terms':{
            #         'field': 'spec.name'
            #     }
            # },
            'source':{
                'terms':{
                    'field': 'source.name',
                    'size' : 5
                },
                "meta": {
                    "title": "Sources",
                    "order": 1,
                }
            },
            # 'language':{
            #     'terms':{'field': 'language'}
            # }
        }
    }
}
"""Introduce searching facets."""


RECORDS_REST_SORT_OPTIONS = {
    'records':{
        'mostrecent': {
            'title': 'Most recent',
            'fields': ['-publication_date'],
            'default_order': 'asc',
            'order': 1,
        },
        'bestmatch': {
            'title': 'Best match',
            'fields': ['-_score'],
            'default_order': 'asc',
            'order': 2,
        },

    }
}
"""Setup sorting options."""


RECORDS_REST_DEFAULT_SORT: {
    'records': {
        'query': 'mostrecent',
        'noquery': 'mostrecent',
    }
}
"""Set default sorting options."""





# Email configuration
# ===================
#: Email address for support.
SUPPORT_EMAIL = "info@iroko.tocororo.cu"
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
#: Enable session/user id request tracing. This feature will add X-Session-ID
#: and X-User-ID headers to HTTP response. You MUST ensure that NGINX (or other
#: proxies) removes these headers again before sending the response to the
#: client. Set to False, in case of doubt.
ACCOUNTS_USERINFO_HEADERS = True



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
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://iroko:iroko@'+IP_POSGRE+'/iroko'

# JSONSchemas
# ===========
#: Hostname used in URLs for local JSONSchemas.
JSONSCHEMAS_HOST = 'iroko.tocororo.cu'

# Flask configuration
# ===================
# See details on
# http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values

#: Secret key - each installation (dev, production, ...) needs a separate key.
#: It should be changed before deploying.
SECRET_KEY = 'iroko_secret_key'
#: Max upload size for form data via application/mulitpart-formdata.
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MiB
#: Sets cookie with the secure flag by default
SESSION_COOKIE_SECURE = True
#: Since HAProxy and Nginx route all requests no matter the host header
#: provided, the allowed hosts variable is set to localhost. In production it
#: should be set to the correct host and it is strongly recommended to only
#: route correct hosts to the application.

WSGI_PROXIES=2


# OAI-PMH
# =======
OAISERVER_ID_PREFIX = 'oai:iroko.tocororo.cu:'

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




# Others iroko configuration
# =======

INIT_TAXONOMY_JSON_PATH = 'data/taxonomy.json'
INIT_JOURNALS_JSON_PATH = 'data/journals.json'
INIT_OAIURL_JSON_PATH = 'data/oaisources.json'



REST_ENABLE_CORS = True
# APP_DEFAULT_SECURE_HEADERS = INVENIO_APP_APP_DEFAULT_SECURE_HEADERS
# APP_DEFAULT_SECURE_HEADERS['content_security_policy'] = {}
# APP_DEFAULT_SECURE_HEADERS['content_security_policy'] = {
#   "default-src": "'self'",
#   "script-src":"'self' 'unsafe-inline' 'unsafe-eval'",
#   "img-src": "'self' data:",
#   "object-src": "'self' ",
#   "style-src":"'self' 'unsafe-inline' 'unsafe-eval' ",
#   "media-src": "'self' ",
#   "child-src": "'self' ",
#   "font-src": "'self' data:"
# }
# TODO: esto de unsafe inline hay que arreglarlo para el deployment to production...
# basicamente esto parece que se debe pasar para el deployment, dentro del role o el playbook de ansible que despliega invenio.
# HARVESTER_DATA_DIRECTORY='data/sceiba-data'
HARVESTER_DATA_DIRECTORY='/mnt/sceiba/sceiba-data'


