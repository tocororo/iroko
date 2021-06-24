# -*- coding: utf-8 -*-

#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

"""Iroko Admin views."""

from flask_admin.contrib.sqla import ModelView

from .models import HarvestedItem, Repository


class RepositoryModelView(ModelView):
    """View for managing vocabularies."""

    # can_view_details = True

    list_all = ('source_uuid', 'harvest_type', 'identifier', 'harvest_endpoint', 'status')

    column_list = list_all

    column_default_sort = ('status', True)

    column_filters = ('harvest_type', 'status')

    form_columns = (
    'harvest_type', 'identifier', 'harvest_endpoint', 'last_harvest_run', 'status', 'error_log')


class HarvestedItemModelView(ModelView):
    """View for managing vocabularies."""

    list_all = ('id', 'source_uuid', 'identifier', 'record', 'status', 'setSpec')

    column_list = list_all

    column_default_sort = ('source_uuid', True)

    column_filters = ('id', 'source_uuid', 'status')

    form_columns = ('identifier', 'status', 'error_log')


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
