# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 UPR.
#
# iroko is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio digital library framework."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

DATABASE = "postgresql"
ELASTICSEARCH = "elasticsearch6"
INVENIO_VERSION = "3.0.0"

tests_require = [
    'check-manifest>=0.35',
    'coverage>=4.4.1',
    'isort>=4.3',
    'mock>=2.0.0',
    'pydocstyle>=2.0.0',
    'pytest-cov>=2.5.1',
    'pytest-invenio>=1.0.2,<1.1.0',
    'pytest-mock>=1.6.0',
    'pytest-pep8>=1.0.6',
    'pytest-random-order>=0.5.4',
    'pytest>=3.3.1',
    'selenium>=3.4.3',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.4.0',
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'Flask-Debugtoolbar>=0.10.1',
    'invenio[{db},{es},base,auth,metadata]~={version}'.format(
        db=DATABASE, es=ELASTICSEARCH, version=INVENIO_VERSION),

]

packages = find_packages()


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
    author_email='info@inveniosoftware.org',
    url='https://github.com/iroko/iroko',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'iroko = invenio_app.cli:cli',
        ],
        'invenio_admin.views': [
            # 'iroko_update_datacite ='
            # 'iroko.modules.records.admin:updatedatacite_adminview'
            'vocabulary_admin = '
            'iroko.modules.taxonomy.admin:vocabularies_adminview',
            'term_admin = '
            'iroko.modules.taxonomy.admin:terms_adminview',
            'source_admin = '
            'iroko.modules.sources.admin:sources_adminview',
            'term_source_admin = '
            'iroko.modules.sources.admin:term_sources_adminview',
            
        ],
        'invenio_db.models': [
            'iroko_taxonomy = iroko.modules.taxonomy.models',
            'iroko_sources = iroko.modules.sources.models',
        ],
        'invenio_base.apps': [
            # 'iroko_communities = '
            # 'iroko.modules.communities.ext:IrokoCommunities',
            # 'iroko_oaiharvester = iroko.modules.oaiharvester.ext:InvenioOAIHarvester',
            # 'iroko_records = iroko.modules.records.ext:IrokoRecords',
            'iroko_app = iroko.ext:IrokoApp',
            'iroko_fixtures = iroko.modules.fixtures.ext:IrokoFixtures',
            'iroko_harvester = iroko.modules.harvester.ext:IrokoHarvester'
        ],
        'invenio_base.api_apps': [
            # 'iroko_communities = '
            # 'iroko.modules.communities.ext:IrokoCommunities',
            # 'iroko_records = iroko.modules.records.ext:IrokoRecords',
        ],
        'invenio_base.api_blueprints' : [
            'iroko_taxonomy = iroko.modules.taxonomy.views:api_blueprint',
            'iroko_sources = iroko.modules.sources.views:api_blueprint'
        ],
        'invenio_celery.tasks': [
            # 'iroko_records = iroko.modules.records.tasks',
        ],
        'invenio_base.blueprints': [
            'iroko = iroko.views:blueprint',
            'iroko_theme = iroko.modules.theme.views:blueprint',
            # 'iroko_communities = iroko.modules.communities.views:blueprint',
        ],
        'invenio_jsonschemas.schemas': [
            # 'iroko_records = iroko.modules.records.jsonschemas',
            # 'iroko_spaces = iroko.modules.orisun.jsonschemas',
            'iroko_documents = iroko.modules.documents.jsonschemas',
        ],
        'invenio_search.mappings': [
            # 'spaces = iroko.modules.orisun.mappings',
            'documents = iroko.modules.documents.mappings',
        ],
        'invenio_pidstore.fetchers': [
            'iroko_documents_fetcher '
            '= iroko.modules.documents.fetchers:document_pid_fetcher',
        ],
        'invenio_pidstore.minters': [
             'iroko_documents_minter '
            '= iroko.modules.documents.minters:document_pid_minter',
        ],
        'invenio_assets.bundles': [
            'iroko_theme_css = iroko.modules.theme.bundles:css',
        ],
        'invenio_config.module': [
            'iroko = iroko.config',
        ],
        'invenio_i18n.translations': [
            'messages = iroko',
        ]
    },
    extras_require=extras_require,
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
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
    ],
)
