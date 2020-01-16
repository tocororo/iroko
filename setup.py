# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 UPR.
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""sceiba project, iroko software, invenio repository software"""

import os

from setuptools import find_packages, setup


readme = open('README.rst').read()

tests_require = [
    'check-manifest>=0.35',
    'coverage>=4.5.3',
    'isort>=4.3',
    'pydocstyle>=3.0.0',
    'pytest-cov>=2.7.1',
    'pytest-invenio>=1.2.1,<1.3.0',
    'pytest-pep8>=1.0.6',
    'pytest>=4.6.4,<5.0.0',
]

db_version = '>=1.0.4,<1.1.0'
search_version = '>=1.2.3,<1.3.0'


extras_require = {
    # Bundles
    # 'invenio-userprofiles>=1.0.1,<1.1.0',

    'base': [
        'invenio-admin>=1.1.2,<1.2.0',
        'invenio-assets>=1.1.3,<1.2.0',
        'invenio-formatter>=1.0.2,<1.1.0',
        'invenio-logging>=1.2.0,<1.3.0',
        'invenio-mail>=1.0.2,<1.1.0',
        'invenio-rest>=1.1.2,<1.2.0',
        'invenio-theme>=1.1.4,<1.2.0',
    ],
    'auth': [
        'invenio-access>=1.3.0,<1.4.0',
        'invenio-accounts>=1.1.1,<1.2.0',
        'invenio-oauth2server>=1.0.4,<1.1.0',
        'invenio-oauthclient>=1.1.3,<1.2.0',
    ],
    'metadata': [
        'invenio-indexer>=1.1.1,<1.2.0',
        'invenio-jsonschemas>=1.0.1,<1.1.0',
        'invenio-oaiserver>=1.1.1,<1.2.0',
        'invenio-pidstore>=1.1.0,<1.2.0',
        'invenio-records-rest>=1.6.4,<1.7.0',
        'invenio-records-ui>=1.0.1,<1.1.0',
        'invenio-records>=1.3.0,<1.4.0',
        'invenio-search-ui>=1.1.1,<1.2.0',
    ],
    'files': [
        'invenio-files-rest>=1.0.5,<1.1.0',
        'invenio-iiif>=1.0.0,<1.1.0',
        'invenio-previewer>=1.1.0,<1.2.0',
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
    # Elasticsearch version
    # 'elasticsearch2': [
    #     'invenio-search[elasticsearch2]{}'.format(search_version),
    # ],
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
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}


setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'Flask>=1.0.4',
    'invenio-app>=1.2.3,<1.3.0',
    'invenio-base>=1.2.0,<1.3.0',
    'invenio-cache>=1.0.0,<1.1.0',
    'invenio-celery>=1.1.1,<1.2.0',
    'invenio-config>=1.0.2,<1.1.0',
    'invenio-i18n>=1.1.1,<1.2.0',
]

# extras_require['all'] = []
for name, reqs in extras_require.items():
    # if name in ('sqlite', 'mysql', 'postgresql') \
    #         or name.startswith('elasticsearch'):
    #     continue
    # extras_require['all'].extend(reqs)
    install_requires.extend(reqs)


packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('iroko', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

print(install_requires)

setup(
    name='iroko',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='iroko Invenio',
    license='MIT',
    author='UPR',
    author_email='info@iroko.tocororo.cu',
    url='https://github.com/tocororo/iroko',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'iroko = invenio_app.cli:cli',
        ],
        'invenio_base.apps': [
            'iroko_records = iroko.records:iroko',
            'iroko_fixtures = iroko.fixtures.ext:IrokoFixtures',
            'iroko_harvester = iroko.harvester.ext:IrokoHarvester',
            'invenio_userprofiles = iroko.userprofiles:InvenioUserProfiles',

        ],
        'invenio_base.blueprints': [
            'iroko = iroko.iroko_theme.views:blueprint',
            'iroko_records = iroko.records.views:blueprint',
            'iroko_curator = iroko.curator.views:blueprint',
            'iroko_texts = iroko.texts.views:blueprint',
            'invenio_userprofiles'
            ' = iroko.userprofiles.views:blueprint_ui_init',

        ],
        'invenio_assets.bundles': [
            'iroko_theme_css = iroko.iroko_theme.bundles:css',
            'iroko_theme_admin_lte_css = iroko.iroko_theme.bundles:admin_lte_css',
            'iroko_theme_admin_css = iroko.iroko_theme.bundles:admin_css',
            'iroko_theme_js = iroko.iroko_theme.bundles:js',
            'iroko_theme_admin_js = iroko.iroko_theme.bundles:admin_js',
        ],
        'invenio_assets.webpack': [
            'iroko_theme = iroko.iroko_theme.webpack:theme',
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
         ],
        'invenio_jsonschemas.schemas': [
            'iroko = iroko.records.jsonschemas'
        ],
        'invenio_search.mappings': [
            'records = iroko.records.mappings'
        ],
        'invenio_admin.views': [
            'vocabulary_admin = iroko.taxonomy.admin:vocabularies_adminview',
            'term_admin = iroko.taxonomy.admin:terms_adminview',
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
        ],
        'invenio_db.models': [
            'iroko_taxonomy = iroko.taxonomy.models',
            'iroko_notification = iroko.notifications.models',
            'iroko_sources = iroko.sources.models',
            'iroko_harvester = iroko.harvester.models',
            'invenio_userprofiles = iroko.userprofiles.models',
        ],
        'invenio_base.api_blueprints' : [
            'iroko_taxonomy = iroko.taxonomy.rest:api_blueprint',
            'iroko_notification = iroko.notifications.rest:api_blueprint',
            'iroko_sources = iroko.sources.rest:api_blueprint',
            'iroko_sources_journals = iroko.sources.journals.rest:api_blueprint',
            'iroko_harvester = iroko.harvester.views:api_blueprint',
            'invenio_userprofiles = iroko.userprofiles.rest:api_blueprint',

        ],
        'invenio_celery.tasks': [
            'iroko_harvester = iroko.harvester.tasks'
        ],
        'invenio_pidstore.fetchers': [
            'irouid'
            '= iroko.pidstore.fetchers:iroko_uuid_fetcher',
        ],
        'invenio_pidstore.minters': [
             'irouid'
            '= iroko.pidstore.minters:iroko_uuid_minter',
        ],
        'invenio_db.alembic': [
            'invenio_userprofiles = iroko.userprofiles:alembic',
        ],
        'invenio_access.actions':[
            'source_editor_actions = iroko.sources.permissions:source_editor_actions',
            'source_gestor_actions = iroko.sources.permissions:source_gestor_actions',            
            'source_full_gestor_actions = iroko.sources.permissions:source_full_gestor_actions',             
            'vocabulary_editor_actions = iroko.taxonomy.permissions:vocabulary_editor_actions',
            'taxonomy_full_editor_actions = iroko.taxonomy.permissions:taxonomy_full_editor_actions',
            'notification_admin_actions = iroko.notifications.permissions:notification_admin_actions',
        ]
    },
    # extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
