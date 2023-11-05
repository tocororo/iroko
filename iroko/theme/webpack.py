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
    default='bootstrap3',
    themes={
        'bootstrap3': dict(
            entry={
                'iroko-theme': './scss/iroko/theme.scss',
                'iroko-preview': './js/iroko/previewer.js',
            },
            dependencies={
                'bootstrap': '3.3.5',
                },
            aliases={},
        ),
        'semantic-ui': dict(
            entry={
                'iroko-preview': './js/iroko/previewer.js',
                # 'iroko_public': './js/iroko/public.js'
                # "theme-admin": "./scss/invenio_theme/admin.scss",
                # "adminlte": "./js/invenio_theme/admin.js",
            },
            dependencies={
                # add any additional npm dependencies here...
                # 'popper.js': '1.16.1',
                # 'jquery': '~3.2.1',
                # 'bootstrap': '~4.5.3',
                # 'font-awesome': '~4.7.0'
            },
            aliases={
                '../../theme.config$': 'less/iroko/theme.config',
            },
        ),
    }
)
