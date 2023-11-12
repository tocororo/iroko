#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
import os

import click
from flask import current_app
from flask.cli import with_appcontext

from iroko.projects.api import ProjectRecord


@click.group()
def projects():
    """Command related to project iroko data."""


@projects.command()
@click.argument('proid')
@with_appcontext
def import_from_file(proid):
    """Load from specific file en data/projects/project.json"""

    datadir = current_app.config['IROKO_DATA_DIRECTORY']
    file_path = os.path.join(datadir, 'projects', 'project.json')
    ProjectRecord.load_from_json_file(file_path, proid)
