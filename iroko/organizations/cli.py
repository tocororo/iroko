#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
import json

import click
from flask.cli import with_appcontext


from iroko.organizations.harvesters.grid import load_grid
from iroko.organizations.harvesters.onei import get_top_organizations, get_lower_organizations
from iroko.organizations.harvesters.wikidata.wikidata import startCollect

from invenio_pidstore.resolver import Resolver
from iroko.organizations.harvesters.general import remove_nulls,_assing_if_exist, insert_in_organizations
from iroko.organizations.api import OrganizationRecord
from invenio_pidstore.errors import PIDAlreadyExists, PIDDoesNotExistError


from iroko.pidstore.pids import ORGANIZATION_PID_TYPE, ORGANIZATION_TYPE


@click.group()
def organizations():
    """Command related to migrating/init iroko data."""

@organizations.command()
@with_appcontext
def import_from_cuor():
    resolver = Resolver(
        pid_type=ORGANIZATION_PID_TYPE,
        object_type=ORGANIZATION_TYPE,
        getter=OrganizationRecord.get_record,
        )

    with open('data/cuor/exportmin1.json') as cuor_file:
        cuor = json.load(cuor_file, object_hook=remove_nulls)
        for org_input in cuor:
            _id = org_input['id']
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