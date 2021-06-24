# -*- coding: utf-8 -*-

#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko Admin views."""

from flask_admin.contrib.sqla import ModelView

from .models import Source, SourceVersion, TermSources


class SourcesModelView(ModelView):
    """View for managing vocabularies."""

    # can_view_details = True

    list_all = ('id', 'name', 'uuid', 'source_type', 'source_status', 'data')

    column_list = list_all

    column_default_sort = ('name', True)

    column_filters = ('name', 'uuid', 'source_type', 'source_status')

    form_columns = ('name', 'source_type', 'source_status')


class SourcesVersionModelView(ModelView):
    list_all = ('id', 'user', 'source_uuid', 'comment', 'created_at', 'is_current')

    column_list = list_all

    column_default_sort = ('created_at', True)

    column_filters = ('user', 'source_uuid', 'comment', 'created_at', 'is_current')

    form_columns = ('user', 'source_uuid', 'comment', 'created_at', 'is_current')


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
    model=Source,
    name='Sources',
    category='Iroko'
    )

sources_version_adminview = dict(
    modelview=SourcesVersionModelView,
    model=SourceVersion,
    name='SourcesVersion',
    category='Iroko'
    )

term_sources_adminview = dict(
    modelview=TermSourcesModelView,
    model=TermSources,
    name='TermSources',
    category='Iroko'
    )

__all__ = ('sources_adminview', 'term_sources_adminview')
