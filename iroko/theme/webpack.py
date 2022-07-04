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
                'iroko-theme': './scss/iroko/theme.scss',
                'iroko-preview': './js/iroko/previewer.js',
            },
            dependencies={},
            aliases={},
        ),
        'semantic-ui': dict(
            entry={
                'iroko-preview': './js/iroko/previewer.js',
            },
            dependencies={
                # add any additional npm dependencies here...
                '@babel/runtime': '^7.9.0',
                '@ckeditor/ckeditor5-build-classic': '^16.0.0',
                '@ckeditor/ckeditor5-react': '^2.1.0',
                'formik': '^2.1.0',
                "i18next": "^20.3.0",
                "i18next-browser-languagedetector": "^6.1.0",
                'luxon': '^1.23.0',
                'path': '^0.12.7',
                'prop-types': '^15.7.2',
                'react-copy-to-clipboard': '^5.0.0',
                'react-dnd': '^11.1.0',
                'react-dnd-html5-backend': '^11.1.0',
                'react-dropzone': "^11.0.0",
                "react-i18next": "^11.11.0",
                'react-invenio-deposit': '^0.19.0',
                'react-invenio-forms': '^0.10.0',
                'react-searchkit': '^2.0.0',
                'yup': '^0.32.0',
            },
            aliases={
                '../../theme.config$': 'less/iroko/theme.config',
                'themes/rdm': 'less/invenio_app_rdm/theme',
                '@less/invenio_app_rdm': 'less/invenio_app_rdm',
                '@translations/invenio_app_rdm':
                    'translations/invenio_app_rdm',
            },
        ),
    }
)
