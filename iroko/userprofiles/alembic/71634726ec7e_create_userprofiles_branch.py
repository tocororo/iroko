# -*- coding: utf-8 -*-

#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Create userprofiles branch."""

# revision identifiers, used by Alembic.
revision = '71634726ec7e'
down_revision = None
branch_labels = (u'invenio_userprofiles',)
depends_on = 'dbdbc1b19cf2'


def upgrade():
    """Upgrade database."""


def downgrade():
    """Downgrade database."""
