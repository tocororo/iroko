# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Pytest fixtures and plugins for the API application."""

from __future__ import absolute_import, print_function

import pytest
from invenio_app.factory import create_api


@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    return create_api
