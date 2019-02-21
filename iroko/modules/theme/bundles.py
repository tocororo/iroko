# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 UPR.
#
# iroko is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""JS/CSS bundles for theme."""

from __future__ import absolute_import, print_function

from flask_assets import Bundle
from invenio_assets import NpmBundle

css = NpmBundle(
    Bundle(
        'scss/styles.scss',
        filters='node-scss, cleancss',
        depends=('scss/*.scss', ),
    ),
    output="gen/iroko.%(version)s.css"
)
"""Default CSS bundle."""
