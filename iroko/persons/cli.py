#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
import json
import os

import click
from flask import current_app
from flask.cli import with_appcontext

from invenio_pidstore.errors import PIDAlreadyExists, PIDDoesNotExistError

from invenio_pidstore.models import  PersistentIdentifier
from iroko.organizations.harvesters.general import (
    insert_in_organizations,
    )
from iroko.utils import _assing_if_exist, remove_nulls

from iroko.pidstore.pids import PERSON_PID_TYPE, IROKO_OBJECT_TYPE
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
