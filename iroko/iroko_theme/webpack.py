# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS bundles for theme.

You include one of the bundles in a page like the example below (using
``base`` bundle as an example):

.. code-block:: html

    {{ webpack['base.js']}}

"""

from __future__ import absolute_import, print_function

from flask_webpackext import WebpackBundle

theme = WebpackBundle(
    __name__,
    'assets',
    entry={
        'iroko_base':        './js/iroko_theme/base.js',
        # requires jquery, moment, select2, bootstrap
        'iroko_adminlte':    './js/iroko_theme/admin.js',
        'iroko_theme-admin': './scss/iroko_theme/admin.scss',
        'iroko_theme':       './scss/iroko_theme/theme.scss',
    },
    dependencies={
        'mdbootstrap':  '~4.8.0',
        'bootstrap':    '~4.3.1',
        'font-awesome': '~4.4.0',
        'jquery':       '~3.2.1',
        'moment':       '~2.23.0',
        'select2':      '~4.0.2',
        'admin-lte':    '~2.4.8',
        'popper.js':    '^1.14.7'
    }
)
