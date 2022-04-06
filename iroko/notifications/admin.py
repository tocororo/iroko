# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko Admin views."""

from flask_admin.contrib.sqla import ModelView

from .models import Notification


class NotificationModelView(ModelView):
    """View for managing notifications."""

    # can_view_details = True

    list_all = ('classification', 'description', 'receiver', 'emiter', 'viewed')

    column_list = list_all

    column_default_sort = ('classification', True)

    column_filters = ('classification', 'description', 'receiver', 'viewed')

    form_columns = ('classification', 'description', 'emiter', 'receiver')


notifications_adminview = dict(
    modelview=NotificationModelView,
    model=Notification,
    name='Notifications',
    category='Iroko'
    )

__all__ = ('notifications_adminview')
