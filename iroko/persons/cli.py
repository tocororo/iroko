#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
import json
import os

import click
from flask import current_app
from flask.cli import with_appcontext

from iroko.organizations.harvesters.grid import load_grid
from iroko.organizations.harvesters.onei import get_top_organizations, get_lower_organizations
from iroko.organizations.harvesters.wikidata.wikidata import startCollect

from invenio_pidstore.resolver import Resolver
from iroko.organizations.harvesters.general import (
    remove_nulls, _assing_if_exist,
    insert_in_organizations,
    )
from iroko.organizations.api import OrganizationRecord
from invenio_pidstore.errors import PIDAlreadyExists, PIDDoesNotExistError

from invenio_pidstore.models import  PersistentIdentifier
from iroko.pidstore.pids import ORGANIZATION_PID_TYPE, IROKO_OBJECT_TYPE

# classification fixtures:
# buscar reeup de mes, minsap, biocubafarma


@click.group()
def persons():
    """Command related to migrating/init iroko data."""

