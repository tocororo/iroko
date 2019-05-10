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

from .models import HarvestedItem, Repository, RepositorySet

class RepositoryModelView(ModelView):
    """View for managing vocabularies."""

    list_all = ('id', 'source_id', 'last_run', 'identifier', 'metadata_formats', 'status')

    column_list = ('id', 'source_id', 'last_run', 'identifier', 'status')

    column_default_sort = ('status', True)

    column_filters = ('id', 'source_id', 'status')
    
    form_columns = ('last_run', 'identifier', 'metadata_formats', 'status', 'error_log')

class RepositorySetModelView(ModelView):
    """View for managing vocabularies."""

    list_all = ('id', 'repository_id', 'setSpec', 'setName')

    column_list = list_all

    column_default_sort = ('repository_id', True)

    column_filters = ('id', 'repository_id')
    
    form_columns = ('repository_id', 'setSpec', 'setName')


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

harvester_repositories_sets_adminview = dict(
    modelview=RepositorySetModelView,
    model=RepositorySet,
    name='Harvester-Repositories-Sets',
    category='Iroko'
)

harvester_items_adminview = dict(
    modelview=HarvestedItemModelView,
    model=HarvestedItem,
    name='Harvester-Items',
    category='Iroko'
)


__all__ = ('harvester_repositories_adminview', 'harvester_repositories_sets_adminview', 'harvester_items_adminview')