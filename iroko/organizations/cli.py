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
    insert_in_organizations,
    )
from iroko.utils import _assing_if_exist, remove_nulls
from iroko.organizations.api import OrganizationRecord
from invenio_pidstore.errors import PIDAlreadyExists, PIDDoesNotExistError

from invenio_pidstore.models import  PersistentIdentifier
from iroko.pidstore.pids import ORGANIZATION_PID_TYPE, IROKO_OBJECT_TYPE

# classification fixtures:
# buscar reeup de mes, minsap, biocubafarma

education_rex = [
    'universidad', 'escuela', 'colegio', 'educacion'
    ]
research_rex = ['investigar', 'universidad', 'centro de estudios']


@click.group()
def organizations():
    """Command related to migrating/init iroko data."""


# In [2]: with open('data/cuor/export_cuor.json') as cuor_file:
#    ...:     cuor = json.load(cuor_file, object_hook=remove_nulls)
#    ...:     for org_input in cuor:
#    ...:         _id = org_input['id']
#    ...:         try:
#    ...:
#    ...:             org, msg = OrganizationRecord.create_or_update(_id, org_input)
#    ...:         except (PIDAlreadyExists) as ex:
#    ...:
#
#


# temporary function to migrate cuor data to iroko.
# arreglar, las org cubanas que solo tienen reup, el anno, en el capo established,
# cambiarlo para onei_registry
@organizations.command()
@with_appcontext
def import_from_cuor():
    resolver = Resolver(
        pid_type=ORGANIZATION_PID_TYPE,
        object_type=IROKO_OBJECT_TYPE,
        getter=OrganizationRecord.get_record,
        )

    datadir = current_app.config['IROKO_DATA_DIRECTORY']
    cuor_path = os.path.join(datadir,'cuor', 'export_all_org_record.json')
    print(cuor_path)
    with open(cuor_path) as cuor_file:
        cuor = json.load(cuor_file, object_hook=remove_nulls)
        for org_input in cuor:
            _id = org_input['id']
            print('------',_id, '------')
            try:
                persistent_identifier, org = resolver.resolve(str(_id))
                if org:
                    print("{0}={1} found".format(ORGANIZATION_PID_TYPE, _id))
                    org.update(org_input)
                    return org, 'updated'
            except Exception:
                try:
                    _id = org_input['id']
                    del org_input['id']
                    org, msg = OrganizationRecord.create_or_update(_id, org_input)
                except (PIDAlreadyExists) as ex:
                    org_input['id'] = _id
                    org, msg = OrganizationRecord.create_or_update(_id, org_input)


@organizations.command()
@with_appcontext
def loadgrid():
    """Load GRID data"""
    load_grid()


@organizations.command()
@with_appcontext
def gettoporg():
    """Load ONEI top organizations data."""
    get_top_organizations()


@organizations.command()
@with_appcontext
def getlowerorg():
    """Load ONEI REEUP organization data"""
    get_lower_organizations()


@organizations.command()
@with_appcontext
def getwikidata(id='Q43229'):
    """Load WIKIDATA organization data"""
    startCollect(id)
