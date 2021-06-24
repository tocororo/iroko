#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import click
from flask.cli import with_appcontext

from iroko.harvester.oai.harvester import OaiHarvester, OaiFetcher


@click.group()
def harvester_oai():
    """Command related to harevest iroko data."""


@harvester_oai.command()
@click.argument('url')
@click.argument('dir')
@with_appcontext
def fetch_url(url, di):
    p = OaiFetcher.fetch_url(url, data_dir=d)
    print('FETCHED {0} into {1}'.format(url, p))


@harvester_oai.command()
@click.argument('l')
@click.argument('d')
@with_appcontext
def fetch_list(l, d):
    file1 = open(l, 'r')
    lines = file1.readlines()
    for line in lines:
        OaiFetcher.fetch_url(line, data_dir=d)


@harvester_oai.command()
@click.argument('d')
@with_appcontext
def fetch_repos(d):
    OaiHarvester.fetch_all_repos(data_dir=d)


@harvester_oai.command()
@click.argument('p')
@with_appcontext
def scan_path(p):
    OaiHarvester.scan_file(p)


@harvester_oai.command()
@with_appcontext
def scan():
    """escanea el directorio HARVESTER_DATA_DIRECTORY"""
    OaiHarvester.scan_dir()


@harvester_oai.command()
@click.argument('d')
@with_appcontext
def scan_dir(d):
    """escanea el directorio d"""
    OaiHarvester.scan_dir(src_dir=d)
