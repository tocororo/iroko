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

from invenio_indexer.api import RecordIndexer
from invenio_oauthclient.contrib import orcid
from invenio_records_rest.facets import terms_filter
from invenio_records_rest.utils import allow_all, check_elasticsearch

from iroko.deployment import *
from iroko.organizations.api import OrganizationRecord
from iroko.organizations.search import OrganizationSearch
from iroko.pidstore import pids as pids
from iroko.records.api import IrokoRecord
from iroko.records.search import IrokoRecordSearch
from iroko.sources.api import IrokoSource
from iroko.sources.search import SourceSearch

basedir = os.path.abspath(os.path.dirname(__file__))


def _(x):
    """Identity function used to trigger string extraction."""
    return x


CACHE_REDIS_URL = 'redis://' + IP_REDIS + ':6379/0'
CACHE_TYPE = 'redis'

# SEARCH_ELASTIC_HOSTS='["http://"]'
params = dict(
    #    http_auth=('user', 'uRTbYRZH268G'),
)
SEARCH_ELASTIC_HOSTS = [
    dict(host=IP_ELASTIC, **params)
]

# Rate limiting
# =============
#: Storage for ratelimiter.
RATELIMIT_STORAGE_URL = 'redis://' + IP_REDIS + ':6379/3'

# I18N
# ====
#: Default language
BABEL_DEFAULT_LANGUAGE = 'en'
#: Default time zone
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
#: Other supported languages (do not include the default language in list).
I18N_LANGUAGES = [
    ('es', _('Spanish')),
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
THEME_FRONTPAGE_TITLE = _('Portal de Publicaciones Científicas Cubanas')
#: Theme logo.
THEME_LOGO = 'images/sceiba-logo.png'
THEME_LOGO_ADMIN = 'images/sceiba-logo.png'
CATALOG_LOGO_ADMIN = 'images/archives_icon_129343.png'
TAXONOMY_LOGO_ADMIN = 'images/checklist_icon_129189.png'
#: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'iroko_theme/frontpage.html'
THEME_JAVASCRIPT_TEMPLATE = 'iroko_theme/javascript.html'

THEME_CONTACT_TEMPLATE = 'iroko_theme/contact.html'

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

# Static page
# ==================
# INIT_STATIC_JSON_PATH = 'static/texts'

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

_RECORD_CONVERTER = (
    'pid(docid, record_class="iroko.records.api:IrokoRecord")'
)
_SOURCE_CONVERTER = (
    'pid(pitmid, record_class="iroko.sources.api:IrokoSource")'
)

RECORDS_REST_ENDPOINTS = dict(
    irouid=dict(
        pid_type=pids.RECORD_PID_TYPE,
        pid_minter=pids.RECORD_PID_MINTER,
        pid_fetcher=pids.RECORD_PID_FETCHER,
        search_class=IrokoRecordSearch,
        record_class=IrokoRecord,
        indexer_class=RecordIndexer,
        record_loaders={
            "application/json": ("iroko.records.loaders"
                                 ":json_v1"),
        },
        record_serializers={
            "application/json": ("iroko.records.serializers"
                                 ":json_v1_response"),
        },
        search_serializers={
            "application/json": ("iroko.records.serializers"
                                 ":json_v1_search"),
        },
        list_route="/records/",
        item_route="/records/<{0}:pid_value>".format(_RECORD_CONVERTER),
        default_media_type="application/json",
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
        list_permission_factory_imp=allow_all,
        suggesters=dict(
            title=dict(
                completion={
                    'field': 'suggest_title'
                }
            )
        )
    ),
    orgid=dict(
        pid_type=pids.ORGANIZATION_PID_TYPE,
        pid_minter=pids.ORGANIZATION_PID_MINTER,
        pid_fetcher=pids.ORGANIZATION_PID_FETCHER,
        search_class=OrganizationSearch,
        record_class=OrganizationRecord,
        indexer_class=RecordIndexer,
        record_loaders={
            "application/json": ("iroko.organizations.loaders"
                                 ":organization_loader_v1"),
        },
        record_serializers={
            "application/json": ("iroko.organizations.serializers"
                                 ":organization_v1_response"),
        },
        search_serializers={
            "application/json": ("iroko.organizations.serializers"
                                 ":organization_v1_search"),
        },
        list_route="/organizations/",
        item_route="/organizations/<{0}:pid_value>".format(_RECORD_CONVERTER),
        default_media_type="application/json",
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
        list_permission_factory_imp=allow_all
    ),
    srcid=dict(
        pid_type=pids.SOURCE_UUID_PID_TYPE,
        pid_minter=pids.SOURCE_UUID_PID_MINTER,
        pid_fetcher=pids.SOURCE_UUID_PID_FETCHER,
        search_class=SourceSearch,
        record_class=IrokoSource,
        indexer_class=RecordIndexer,
        record_loaders={
            "application/json": ("iroko.sources.marshmallow.source_v1"
                                 ":source_loader_v1"),
        },
        record_serializers={
            "application/json": ("iroko.sources.marshmallow.source_v1"
                                 ":source_v1_response"),
        },
        search_serializers={
            "application/json": ("iroko.sources.marshmallow.source_v1"
                                 ":source_v1_search"),
        },
        list_route="/sources/",
        item_route="/sources/<{0}:pid_value>".format(_SOURCE_CONVERTER),
        default_media_type="application/json",
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
        list_permission_factory_imp=allow_all,
    )
)

"""REST API for iroko."""

PIDSTORE_RECID_FIELD = 'id'

IROKO_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""

RECORDS_REST_FACETS = dict(
    records=dict(
        filters=dict(
            keywords=terms_filter('keywords'),
            creators=terms_filter('creators.name'),
            sources=terms_filter('source.name'),
            status=terms_filter('status'),
            terms=terms_filter('terms')
        ),
        aggs=dict(
            keywords=dict(
                terms=dict(
                    field='keywords',
                    size=5
                ),
                meta=dict(
                    title=_("Keywords"),
                    order=3
                )
            ),
            creators=dict(
                terms=dict(
                    field='creators.name',
                    size=5
                ),
                meta=dict(
                    title=_("Creators"),
                    order=2
                )
            ),
            terms=dict(
                terms=dict(
                    field='terms'
                )
            ),
            sources=dict(
                terms=dict(
                    field='source.name',
                    size=5
                ),
                meta=dict(
                    title=_("Sources"),
                    order=1
                )
            )
        )
    ),
    organizations=dict(
        filters=dict(
            status=terms_filter('status'),
            types=terms_filter('types'),
            country=terms_filter('country'),
            state=terms_filter('state'),
        ),
        aggs=dict(
            status=dict(
                terms=dict(
                    field='status',
                    size=5
                )
            ),
            types=dict(
                terms=dict(
                    field='types',
                    size=8
                )
            ),
            country=dict(
                terms=dict(
                    field='addresses.country',
                    size=8
                )
            ),
            state = dict(
                terms=dict(
                    field='addresses.state',
                    size=5
                )
            )
        )
    ),
    sources=dict(
        filters=dict(
            source_type=terms_filter('source_type'),
            source_status=terms_filter('source_status'),
            relations=terms_filter('relations.uuid')
        ),
        aggs=dict(
            source_type=dict(
                terms=dict(
                    field='source_type',
                    size=5
                )
            ),
            source_status=dict(
                terms=dict(
                    field='source_status',
                    size=5
                )
            )
        )
    )
)
"""Introduce searching facets."""

RECORDS_REST_SORT_OPTIONS = {
    'records': {
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
MAIL_SERVER = SMTP_SERVER
MAIL_PORT = SMTP_PORT
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = SMTP_USERNAME
MAIL_PASSWORD = SMTP_PASSWORD
MAIL_DEFAULT_SENDER = SMTP_DEFAULT_SENDER
# MAIL_MAX_EMAILS = default None
# MAIL_ASCII_ATTACHMENTS = default False


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
ACCOUNTS_SESSION_REDIS_URL = 'redis://' + IP_REDIS + ':6379/1'
#: Enable session/user id request tracing. This feature will add X-Session-ID
#: and X-User-ID headers to HTTP response. You MUST ensure that NGINX (or other
#: proxies) removes these headers again before sending the response to the
#: client. Set to False, in case of doubt.
ACCOUNTS_USERINFO_HEADERS = True

# Celery configuration
# ====================

BROKER_URL = 'amqp://iroko:iroko@' + IP_RABBIT + ':5672/'
#: URL of message broker for Celery (default is RabbitMQ).
CELERY_BROKER_URL = 'amqp://iroko:iroko@' + IP_RABBIT + ':5672/'
#: URL of backend for result storage (default is Redis).
CELERY_RESULT_BACKEND = 'redis://' + IP_REDIS + ':6379/2'
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
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# Database
# ========
#: Database URI including user and password
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://iroko:iroko@' + IP_POSGRE + '/iroko'

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

WSGI_PROXIES = 2

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


REST_ENABLE_CORS = True

OAUTHCLIENT_REMOTE_APPS = dict(
    orcid=orcid.REMOTE_APP,
)

OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 86400

APP_DEFAULT_SECURE_HEADERS = {
    'force_https': True,
    'force_https_permanent': False,
    'force_file_save': False,
    'frame_options': 'sameorigin',
    'frame_options_allow_from': None,
    'strict_transport_security': True,
    'strict_transport_security_preload': False,
    'strict_transport_security_max_age': 31556926,  # One year in seconds
    'strict_transport_security_include_subdomains': True,
    'content_security_policy': {
        'default-src': ["'self'", "'unsafe-inline'"],
        'object-src': ["'none'"],
        'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'font-src': ["'self'", "data:"],
        'img-src': ["'self'", "data:"]
    },
    'content_security_policy_report_uri': None,
    'content_security_policy_report_only': False,
    'session_cookie_secure': True,
    'session_cookie_http_only': True
}

#
# Variables para OAIServer
#

OAISERVER_ADMIN_EMAILS = [
    'rafael.martinez@upr.edu.cu',
    'eduardo.arencibia@upr.edu.cu'
]

OAISERVER_RECORD_INDEX = '_all'
OAISERVER_ID_PREFIX = 'oai:localhost:records/'
OAISERVER_QUERY_PARSER_FIELDS = ["title_statement"]

# Iroko Vocabularies
