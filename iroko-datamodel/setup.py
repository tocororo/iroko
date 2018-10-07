# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 UPR.
#
# iroko datamodel is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Iroko data model"""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.3.3',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

invenio_search_version = '1.0.0'
invenio_db_version = '1.0.1'

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    # Elasticsearch version
    'elasticsearch5': [
        'invenio-search[elasticsearch5]>={}'.format(invenio_search_version),
    ],
    'elasticsearch6': [
        'invenio-search[elasticsearch6]>={}'.format(invenio_search_version),
    ],
    # Databases
    'mysql': [
        'invenio-db[mysql]>={}'.format(invenio_db_version),
    ],
    'postgresql': [
        'invenio-db[postgresql]>={}'.format(invenio_db_version),
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name[0] == ':' or name in ('elasticsearch5', 'elasticsearch6', 'mysql',
                                  'postgresql'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'invenio-records-rest>=1.1.0,<1.2.0',
    'arrow>=0.12.1',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('iroko_datamodel', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='iroko-datamodel',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='iroko-datamodel Invenio',
    license='MIT',
    author='UPR',
    author_email='rafael.martinez@upr.edu.cu',
    url='https://github.com/tocororo/iroko-datamodel',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'iroko_datamodel = iroko_datamodel:irokodatamodel',
        ],
        'invenio_base.api_apps': [
            'iroko_datamodel = iroko_datamodel:irokodatamodel',
        ],
        'invenio_base.blueprints': [
            'iroko_datamodel = iroko_datamodel.views:blueprint',
        ],
        'invenio_jsonschemas.schemas': [
            'iroko_datamodel = iroko_datamodel.jsonschemas'
        ],
        'invenio_search.mappings': [
            'records = iroko_datamodel.mappings'
        ],
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
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Planning',
    ],
)
