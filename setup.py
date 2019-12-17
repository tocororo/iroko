# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 UPR.
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""sceiba project, iroko software, invenio repository softwar"""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

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

        ],
        'invenio_base.blueprints': [
            'iroko = iroko.iroko_theme.views:blueprint',
            'iroko_records = iroko.records.views:blueprint',
            'iroko_curator = iroko.curator.views:blueprint',
            'iroko_texts = iroko.texts.views:blueprint',
            'iroko_sources = iroko.sources.views:blueprint',

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
        ],
        'invenio_base.api_apps': [
            'iroko = iroko.records:iroko',

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
            'source_admin = iroko.sources.admin:sources_adminview',
            'source_version_admin = iroko.sources.admin:sources_version_adminview',
            'term_source_admin = iroko.sources.admin:term_sources_adminview',
            'harvester_items_adminview = '
            'iroko.harvester.admin:harvester_items_adminview',
        ],
        'invenio_db.models': [
            'iroko_taxonomy = iroko.taxonomy.models',
            'iroko_sources = iroko.sources.models',
            'iroko_harvester = iroko.harvester.models',
        ],
        'invenio_base.api_blueprints' : [
            'iroko_taxonomy = iroko.taxonomy.rest:api_blueprint',
            'iroko_sources = iroko.sources.rest:api_blueprint',
            'iroko_sources = iroko.sources.journals.rest:api_blueprint'
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
    },
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
