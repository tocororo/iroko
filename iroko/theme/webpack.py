# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    'assets',
    default='semantic-ui',
    themes={
        'bootstrap3': dict(
            entry={
                'iroko-theme': './scss/iroko/theme.scss',
                'iroko-preview': './js/iroko/previewer.js',
            },
            dependencies={ },
            aliases={},
        ),
        'semantic-ui': dict(
            entry={
                'iroko-preview': './js/iroko/previewer.js',
            },
            dependencies={
                # add any additional npm dependencies here...
                "i18next": "^20.3.0",
                "i18next-browser-languagedetector": "^6.1.0",
                "react-i18next": "^11.11.0",
                },
            aliases={
                '../../theme.config$': 'less/iroko/theme.config',
            },
        ),
    }
)
