# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 UPR.
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
                'testinv-theme': './scss/testinv/theme.scss',
                'testinv-preview': './js/testinv/previewer.js',
            },
            dependencies={},
            aliases={},
        ),
        'semantic-ui': dict(
            entry={
                'testinv-preview': './js/testinv/previewer.js',
            },
            dependencies={
                # add any additional npm dependencies here...
            },
            aliases={
                '../../theme.config$': 'less/testinv/theme.config',
            },
        ),
    }
)
