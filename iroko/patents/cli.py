#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
import os

import click
from flask import current_app
from flask.cli import with_appcontext

from iroko.patents.api import PatentRecord


@click.group()
def patents():
    """Command related to patents iroko data."""


@patents.command()
@click.argument('patid')
@with_appcontext
def import_from_file(patid):
    """Load from specific file en data/patents/patents.json"""

    datadir = current_app.config['IROKO_DATA_DIRECTORY']
    file_path = os.path.join(datadir, 'patents', 'patents.json')
    PatentRecord.load_from_json_file(file_path, patid)
