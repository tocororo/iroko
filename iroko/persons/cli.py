#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
import json
import os

import click
from flask import current_app
from flask.cli import with_appcontext

from invenio_pidstore.resolver import Resolver
from invenio_pidstore.errors import PIDAlreadyExists, PIDDoesNotExistError

from invenio_pidstore.models import  PersistentIdentifier


@click.group()
def persons():
    """Command related to migrating/init iroko data."""

