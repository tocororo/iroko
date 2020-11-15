"""Manage fixtures for INSPIRE site."""

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
