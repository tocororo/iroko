"""Curator APIs."""

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, print_function

import uuid

from invenio_db import db
# from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore


# from invenio_records.api import Record


def create_vocabulary(data):
    """Create a vocabulary

    :param dict data: The vocabulary data.
    """
    with db.session.begin_nested():
        # create uuid
        rec_uuid = uuid.uuid4()
        # create PID
        current_pidstore.minters['recid'](rec_uuid, data)
        # create record
        # created_record = Record.create(data, id_=rec_uuid)
        # index the record
        # RecordIndexer().index(created_record)
    db.session.commit()
