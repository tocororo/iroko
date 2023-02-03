# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko Admin views."""

from flask_admin.contrib.sqla import ModelView

from .models import Evaluation


class EvaluationModelView(ModelView):
    """View for managing evaluations."""

    # can_view_details = True


    list_all = ('id','uuid','state', 'datetime', 'notes', 'user', 'data')

    column_list = list_all

    column_default_sort = ('state', True)

    column_filters = ('state', 'datetime', 'notes', 'user')

    form_columns = ('state', 'datetime', 'notes', 'user', 'data')


evaluation_adminview = dict(
    modelview=EvaluationModelView,
    model=Evaluation,
    name='Evaluation',
    category='Iroko'
    )

__all__ = ('evaluation_adminview')
