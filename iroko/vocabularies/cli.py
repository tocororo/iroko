#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, division, print_function

import click
from flask.cli import with_appcontext

from iroko.vocabularies.fixtures import init_taxonomy


@click.group()
def vocabularies():
    """Command related to Iroko Vocabularies"""


@vocabularies.command()
@with_appcontext
def init_vocabs():
    """Init vocabularies."""
    init_taxonomy()
