#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, division, print_function

import click
from flask.cli import with_appcontext
from invenio_db import db
from invenio_records_files.models import RecordsBuckets
from iroko.records.search import IrokoRecordSearch
from iroko.records.api import IrokoRecord

@click.group()
def records():
    """Command related to Iroko Records"""


@records.command()
@with_appcontext
def add_bundles_to_update():
    search = IrokoRecordSearch()
    for hit in search.scan():
        record = IrokoRecord.get_record_by_pid_value(hit.id)
        if not hasattr(record, 'bucket_id'):
            bucket = IrokoRecord.create_bucket(record)
            if bucket:
                # Attach bucket to the record
                IrokoRecord.dump_bucket(record, bucket)
                RecordsBuckets.create(record=record.model, bucket=bucket)
                record.commit()
    db.session.commit()

