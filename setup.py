# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 UPR.
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.
#flask-swagger-ui              4.11.1
#ully installed apispec-5.1.1

"""sceiba.cu backend source code"""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
tests_require = [
    'pytest-invenio>=1.4.0,<1.5.0',
]

db_version = '>=1.0.9,<1.1.0'
search_version = '>=1.4.2,<1.5.0'

extras_require = {
    # Bundles
    'base': [
        'invenio-admin>=1.3.2,<1.4.0',
        'invenio-assets>=1.2.7,<1.3.0',
        'invenio-formatter>=1.1.3,<1.2.0',
        'invenio-logging>=1.3.0,<1.4.0',
        'invenio-mail>=1.0.2,<1.1.0',
        'invenio-rest>=1.2.8,<1.3.0',
        'invenio-theme>=1.3.17,<1.4.0',
    ],
    'auth': [
        'invenio-access>=1.4.2,<1.5.0',
        'invenio-accounts>=1.4.11,<1.5.0',
        'invenio-oauth2server>=1.3.5,<1.4.0',
        'invenio-oauthclient>=1.5.3,<1.6.0',
        # 'invenio-userprofiles>=1.2.4,<1.3.0',
    ],
    'metadata': [
        'invenio-indexer>=1.2.1,<1.3.0',
        'invenio-jsonschemas>=1.1.4,<1.2.0',
        'invenio-oaiserver>=1.4.0,<1.5.0',
        'invenio-pidstore>=1.2.3,<1.3.0',
        'invenio-records-rest>=1.9.0,<1.10.0',
        'invenio-records-ui>=1.2.0,<1.3.0',
        'invenio-records>=1.6.1,<1.7.0',
        'invenio-search-ui<2.0.6',
    ],
    'files': [
        'invenio-files-rest>=1.3.2,<1.4.0',
        'invenio-iiif>=1.2.0,<1.3.0',
        'invenio-previewer>=1.3.2,<1.4.0',
        'invenio-records-files>=1.2.1,<1.3.0',
    ],
    # Database version
    'postgresql': [
        'invenio-db[postgresql,versioning]{}'.format(db_version),
    ],
    # 'mysql': [
    #     'invenio-db[mysql,versioning]{}'.format(db_version),
    # ],
    # 'sqlite': [
    #     'invenio-db[versioning]{}'.format(db_version),
    # ],
    # # Elasticsearch version
    # 'elasticsearch5': [
    #     'invenio-search[elasticsearch5]{}'.format(search_version),
    # ],
    'elasticsearch6': [
        'invenio-search[elasticsearch6]{}'.format(search_version),
    ],
    # 'elasticsearch7': [
    #     'invenio-search[elasticsearch7]{}'.format(search_version),
    # ],
    # Docs and test dependencies
    'docs': [
        'Sphinx>=4.2.0,<5',
    ],
    'tests': tests_require,
}

# extras_require['all'] = []
# for name, reqs in extras_require.items():
#     if name in ('sqlite', 'mysql', 'postgresql') \
#             or name.startswith('elasticsearch'):
#         continue
#     extras_require['all'].extend(reqs)


install_requires = [
    'invenio-app>=1.3.3,<1.4.0',
    'invenio-base>=1.2.9,<1.3.0',
    'invenio-cache>=1.1.0,<1.2.0',
    'invenio-celery>=1.2.4,<1.3.0',
    'invenio-config>=1.0.3,<1.1.0',
    'invenio-i18n>=1.3.1,<1.4.0',
]

packages = find_packages()

# extras_require['all'] = []
for name, reqs in extras_require.items():
    # if name in ('sqlite', 'mysql', 'postgresql') \
    #         or name.startswith('elasticsearch'):
    #     continue
    # extras_require['all'].extend(reqs)
    install_requires.extend(reqs)

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('iroko', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='iroko',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='iroko Invenio',
    license='MIT',
    author='UPR',
    author_email='sceiba.cu@gmail.com',
    url='https://github.com/tocororo/iroko',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    # install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'iroko = invenio_app.cli:cli',
        ],
        'invenio_base.apps': [
            'iroko_records = iroko.records:iroko',
            'iroko_sources = iroko.sources.ext:IrokoSources',
            'iroko_vocabularies= iroko.vocabularies.ext:IrokoVocabularies',
            'iroko_harvester = iroko.harvester.ext:IrokoHarvester',
            'invenio_userprofiles = iroko.userprofiles:InvenioUserProfiles',
            'iroko_organizations = iroko.organizations.ext:IrokoOrganizations',
            'iroko_persons = iroko.persons.ext:IrokoPersons',
        ],
        'invenio_base.blueprints': [
            'iroko = iroko.theme.views:blueprint',
            'iroko_records = iroko.records.views:blueprint',
            'iroko_curator = iroko.curator.views:blueprint',
            'iroko_internal_apps = iroko.auth.internal_apps:blueprint',
            'invenio_userprofiles'
            ' = iroko.userprofiles.views:blueprint_ui_init',
            'iroko_swagger = iroko.docs.views:swagger_blueprint',
            'iroko_apispec = iroko.docs.views:apispec_blueprint',
        ],
        'invenio_assets.webpack': [
            'iroko_theme = iroko.theme.webpack:theme',
        ],
        'invenio_config.module': [
            'iroko = iroko.config',
        ],
        'invenio_i18n.translations': [
            'messages = iroko',
            'messages_userprofiles = iroko.userprofiles',
        ],
        'invenio_base.api_apps': [
            'iroko = iroko.records:iroko',
            'invenio_userprofiles = iroko.userprofiles:InvenioUserProfiles',
            'iroko_organizations = iroko.organizations:IrokoOrganizations',
            'iroko_persons = iroko.persons:IrokoPersons',
         ],
        'invenio_jsonschemas.schemas': [
            'iroko = iroko.records.jsonschemas',
            'sources = iroko.sources.schemas',
            'organizations = iroko.organizations.jsonschemas',
            'persons = iroko.persons.jsonschemas',
        ],
        'invenio_search.mappings': [
            'records = iroko.records.mappings',
            'sources = iroko.sources.mappings',
            'organizations = iroko.organizations.mappings',
            'persons = iroko.persons.mappings',
        ],
        'invenio_admin.views': [
            'vocabulary_admin = iroko.vocabularies.admin:vocabularies_adminview',
            'term_admin = iroko.vocabularies.admin:terms_adminview',
            'notification_admin = iroko.notifications.admin:notifications_adminview',
            'source_admin = iroko.sources.admin:sources_adminview',
            'source_version_admin = iroko.sources.admin:sources_version_adminview',
            'term_source_admin = iroko.sources.admin:term_sources_adminview',
            'harvester_repositories_adminview = '
            'iroko.harvester.admin:harvester_repositories_adminview',
            'harvester_items_adminview = '
            'iroko.harvester.admin:harvester_items_adminview',
            'invenio_userprofiles_view = '
            'iroko.userprofiles.admin:user_profile_adminview',
            'evaluations_admin = iroko.evaluations.admin:evaluation_adminview',
            ],
        'invenio_db.models': [
            'iroko_taxonomy = iroko.vocabularies.models',
            'iroko_notification = iroko.notifications.models',
            'iroko_sources = iroko.sources.models',
            'iroko_harvester = iroko.harvester.models',
            'invenio_userprofiles = iroko.userprofiles.models',
            'iroko_evaluations = iroko.evaluations.models',
            ],
        'invenio_base.api_blueprints': [
            'iroko_taxonomy = iroko.vocabularies.rest:api_blueprint',
            'iroko_notification = iroko.notifications.rest:api_blueprint',
            'iroko_sources = iroko.sources.rest:api_blueprint',
            'iroko_sources_journals = iroko.sources.journals.rest:api_blueprint',
            'iroko_harvester = iroko.harvester.rest:api_blueprint',
            'invenio_userprofiles = iroko.userprofiles.rest:api_blueprint',
            'iroko_records = iroko.records.rest:api_blueprint',
            'iroko_organizations = iroko.organizations.rest:api_blueprint',
            'iroko_persons = iroko.persons.rest:api_blueprint',
            'iroko_evaluations = iroko.evaluations.rest:api_blueprint',
            'iroko_utils = iroko.rest:api_blueprint'
            ],
        'invenio_celery.tasks': [
            'iroko_harvester = iroko.harvester.tasks'
            ],
        'invenio_pidstore.fetchers': [
            'irouid = iroko.pidstore.fetchers:iroko_uuid_fetcher',
            'recids = iroko.pidstore.fetchers:iroko_record_identifiers_fetcher',
            'recoai = iroko.pidstore.fetchers:iroko_source_oai_fetcher',
            'srcid = iroko.pidstore.fetchers:iroko_source_uuid_fetcher',
            'orgid = iroko.pidstore.fetchers:organization_uuid_fetcher',
            'perid = iroko.pidstore.fetchers:person_uuid_fetcher',
            ],
        'invenio_pidstore.minters': [
            'irouid = iroko.pidstore.minters:iroko_uuid_minter',
            'recids = iroko.pidstore.minters:iroko_record_identifiers_minter',
            'recoai = iroko.pidstore.minters:iroko_source_oai_minter',
            'srcid = iroko.pidstore.minters:iroko_source_uuid_minter',
            'orgid = iroko.pidstore.minters:organization_uuid_minter',
            'perid = iroko.pidstore.minters:person_uuid_minter',
            ],
        'invenio_db.alembic': [
            'invenio_userprofiles = iroko.userprofiles:alembic',
            ],
        'invenio_access.actions': [
            'source_editor_actions = iroko.sources.permissions:source_editor_actions',
            'sourceactions = iroko.sources.permissions:source_manager_actions',
            'source_full_manager_actions = iroko.sources.permissions:source_full_manager_actions',
            'source_term_manager_actions = iroko.sources.permissions:source_term_manager_actions',
            'source_organization_manager_actions = '
            'iroko.sources.permissions:source_organization_manager_actions',
            'vocabulary_editor_actions = iroko.vocabularies.permissions:vocabulary_editor_actions',
            'vocabularies_full_editor_actions = '
            'iroko.vocabularies.permissions:vocabularies_full_editor_actions',
            'notification_admin_actions = '
            'iroko.notifications.permissions:notification_admin_actions',
            'notification_viewed_actions = '
            'iroko.notifications.permissions:notification_viewed_actions',
            'evaluation_admin_actions = '
            'iroko.evaluations.permissions:evaluation_admin_actions',
            'evaluation_viewed_actions = '
            'iroko.evaluations.permissions:evaluation_viewed_actions',
            ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 3 - Alpha',
    ],
)
