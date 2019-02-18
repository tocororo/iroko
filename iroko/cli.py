# -*- coding: utf-8 -*-
#
# This file is part of iroko
# Copyright (C) 2018 UPR.
#


"""Click command-line interface for iroko management."""

from __future__ import absolute_import, print_function

import json
import sys

import click

from flask import current_app
from flask.cli import with_appcontext

from .modules.orisun.api import Space

@click.group()
def irokoapp():
    """iroko app commands."""



@irokoapp.command()
@click.argument('source', type=click.File('r'), default=sys.stdin)
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.option('-s', '--vendor', 'vendor', default='cantook')
@with_appcontext
def init(source, verbose, vendor):
    """Init iroko."""
    click.secho('Init all sources, harvest config, and set schedule for start harvesting:', fg='green')
    data = json.load(source)
    
#     click.echo("data = json.load("+str(source)+")")

    if isinstance(data, dict):
        for k, record in data.items():
            click.echo(str(record["title"]))
            record, status = Space.create_or_update(
                record, vendor=vendor, dbcommit=True, reindex=True
            )
            click.echo('record uuid: ' + str(record.id) + ' | ' + status)

@irokoapp.command()
@click.argument('source', type=click.File('r'), default=sys.stdin)
@click.argument('taxonomy', type=click.File('r'), default=sys.stdin)
@click.argument('dest', type=click.File('w'), default=sys.stdout)
@with_appcontext
def fixjournal(source, taxonomy,dest):
    """Init iroko."""
    click.secho('fix json with taxonomy... ', fg='green')
    data = json.load(source, object_hook=remove_nulls)
    tax = json.load(taxonomy)
#     json.dump()

    if isinstance(data, dict):
        for k, record in data.items():
            if "source_category" in record:
                cat = record["source_category"]
                record["source_category"] = tax["grupo-mes"][cat]["name"]
            if "year_start" in record:
                record["year_start"] = str(record["year_start"])

            if "year_end" in record:
                record["year_end"] = str(record["year_end"])


            if "institution" in record:
                inst = record["institution"]
                record["institution"] = tax["organismos"][inst]["name"]

            if "subjects" in record:
                subtexts = []
                for subid in record["subjects"]:
                    subtexts.append(tax["tematicas"][subid]["name"])
                    record["subjects"] = subtexts
            else:
                click.echo(str(record))

            if "licence" in record:
                licence = record["licence"]
                record["licence"] = tax["licencias"][licence]["name"]

            if "referecences" in record:
                reftexts = []
                for ref in record["referecences"]:
                    reffix = {
                        "name": tax["data_bases"][ref["name"]]["name"]
                    }
                    if "url" in ref:
                        reffix.update({"url": ref["url"]})
                        reftexts.append(reffix)
                record["referecences"] = reftexts

    json.dump(data,dest, ensure_ascii=False)


def remove_nulls(d):
    return {k: v for k, v in d.items() if v is not None}        
        # record, status = Space.create_or_update(
        #     record, vendor=vendor, dbcommit=True, reindex=True
        # )
        # click.echo('record uuid: ' + str(record.id) + ' | ' + status)

# def get_text(self, tax):
#         pass