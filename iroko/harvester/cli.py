#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import click
from flask.cli import with_appcontext

from iroko.harvester.oai.harvester import OaiFetcher, OaiHarvester
from iroko.harvester.tasks import iroko_test_task


@click.group()
def harvester():
    """Command related to harevest iroko data."""


@harvester.command()
@click.argument('url')
@click.argument('dir')
@with_appcontext
def fetch_url(url, dir):
    p = OaiFetcher.fetch_url(url, data_dir=dir)
    print('FETCHED {0} into {1}'.format(url, p))


@harvester.command()
@click.argument('l')
@click.argument('d')
@with_appcontext
def fetch_list(l, d):
    file1 = open(l, 'r')
    lines = file1.readlines()
    for line in lines:
        OaiFetcher.fetch_url(line, data_dir=d)


@harvester.command()
@click.argument('d')
@with_appcontext
def fetch_repos(d):
    OaiHarvester.fetch_all_repos(data_dir=d)


@harvester.command()
@click.argument('p')
@with_appcontext
def scan_path(p):
    OaiHarvester.scan_file(p)


@harvester.command()
@with_appcontext
def scan():
    """escanea el directorio HARVESTER_DATA_DIRECTORY"""
    OaiHarvester.scan_dir()


@harvester.command()
@click.argument('d')
@with_appcontext
def scan_dir(d):
    """escanea el directorio d"""
    print(d)
    OaiHarvester.scan_dir(src_dir=d)


@harvester.command()
@click.argument('upto')
@with_appcontext
def test(upto):
    celery_kwargs = {
        'kwargs': {
            'upto': upto,
            }
        }
    iroko_test_task.apply_async(**celery_kwargs)
