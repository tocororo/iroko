#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
import os

import click
from flask import current_app
from flask.cli import with_appcontext

from iroko.persons.api import PersonRecord


@click.group()
def persons():
    """Command related to persons iroko data."""


@persons.command()
@click.argument('orgid')
@with_appcontext
def import_from_file(orgid):
    """Load from specific file en data/persons/persons.json"""

    datadir = current_app.config['IROKO_DATA_DIRECTORY']
    file_path = os.path.join(datadir, 'persons', 'persons.json')
    PersonRecord.load_from_json_file(file_path, orgid)
