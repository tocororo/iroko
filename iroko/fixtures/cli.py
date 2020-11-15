# -*- coding: utf-8 -*-

#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from __future__ import absolute_import, division, print_function

import click
from flask.cli import with_appcontext



@click.group()
def fixtures():
    """Command related to migrating/init iroko data."""
#
#
# @fixtures.command()
# @with_appcontext
# def initvocabs():
#     """Init vocabularies."""
#     init_taxonomy()
#
#
# @fixtures.command()
# @with_appcontext
# def initjournals():
#     """Init journals."""
#     init_journals()
#
#
# @fixtures.command()
# @with_appcontext
# def initjournalsrelations():
#     """Init journals relations with terms."""
#     init_term_sources()
