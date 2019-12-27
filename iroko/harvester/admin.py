# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017, 2018 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Iroko Admin views."""

from flask_admin.contrib.sqla import ModelView

from .models import HarvestedItem, Repository


class RepositoryModelView(ModelView):
    """View for managing vocabularies."""

    # can_view_details = True

    list_all = ('id', 'source', 'harvest_type', 'identifier', 'harvest_endpoint', 'status')

    column_list = list_all

    column_default_sort = ('status', True)

    column_filters = ('harvest_type','status')

    form_columns = ('source', 'harvest_type', 'identifier', 'harvest_endpoint', 'last_harvest_run', 'status', 'error_log')


class HarvestedItemModelView(ModelView):
    """View for managing vocabularies."""

    list_all = ('id', 'repository_id', 'identifier', 'record', 'status', 'setSpec')

    column_list = list_all

    column_default_sort = ('repository_id', True)

    column_filters = ('id', 'repository_id', 'status')

    form_columns = ('identifier', 'status','error_log')


harvester_repositories_adminview = dict(
    modelview=RepositoryModelView,
    model=Repository,
    name='Harvester-Repositories',
    category='Iroko'
)
harvester_items_adminview = dict(
    modelview=HarvestedItemModelView,
    model=HarvestedItem,
    name='Harvester-Items',
    category='Iroko'
)


__all__ = ('harvester_items_adminview')
