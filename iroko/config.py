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

from .dev_ip import IP_ELASTIC, IP_POSGRE, IP_RABBIT, IP_REDIS, APP_ALLOWED_HOSTS
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
    # ('fr', _('French'))
]

# Base templates
# ==============
#: Global base template.
BASE_TEMPLATE = 'iroko/page.html'
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



INIT_TAXONOMY_JSON_PATH = 'data/taxonomy.json'
INIT_JOURNALS_JSON_PATH = 'data/journals.json'
INIT_OAIURL_JSON_PATH = 'data/oaisources.json'



REST_ENABLE_CORS = True

HARVESTER_DATA_DIRECTORY='/opt/sceiba-data'
