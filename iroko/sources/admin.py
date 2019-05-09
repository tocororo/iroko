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

from .models import Sources, TermSources

class SourcesModelView(ModelView):
    """View for managing vocabularies."""

    # can_view_details = True

    list_all = ('id', 'name', 'uuid', 'source_type', 'harvest_type', 'harvest_endpoint')

    column_list = list_all

    column_default_sort = ('name', True)

    column_filters = ('id', 'name', 'source_type', 'harvest_type','harvest_endpoint')

    form_columns = ('name', 'source_type', 'harvest_type', 'harvest_endpoint', 'data')

class TermSourcesModelView(ModelView):
    """View for managing terms."""

    # can_view_details = True

    list_all = ('source', 'term')

    column_list = list_all

    # column_default_sort = ('source', True)

    column_filters = list_all

    # form_columns = ('name', 'description')
    form_columns = ('source', 'term')


sources_adminview = dict(
    modelview=SourcesModelView,
    model=Sources,
    name='Sources',
    category='Iroko'
)

term_sources_adminview = dict(
    modelview=TermSourcesModelView,
    model=TermSources,
    name='TermSources',
    category='Iroko'
)

__all__ = ('sources_adminview', 'term_sources_adminview')