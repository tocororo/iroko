"""E2E test of the front page."""

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

from flask import url_for


def test_frontpage(live_server, browser):
    """Test retrieval of front page."""
    browser.get(url_for('iroko_theme_frontpage.index', _external=True))
    assert "Welcome to iroko." == browser.find_element_by_class_name(
        'marketing').find_element_by_tag_name('h1').text
