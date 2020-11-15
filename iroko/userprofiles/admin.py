# -*- coding: utf-8 -*-

#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

#
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Admin views for invenio-userprofiles."""

from __future__ import absolute_import, print_function

import json

from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup

from .models import UserProfile


def _(x):
    """Identity."""
    return x


def json_formatter(view, context, model, name):
    value = getattr(model, name)
    json_value = json.dumps(value, ensure_ascii=False, indent=2)
    return Markup('<pre>{}</pre>'.format(json_value))


class UserProfileView(ModelView):
    """Userprofiles view. Links User ID to user/full/display name."""

    can_view_details = True
    can_create = False
    can_delete = False

    column_list = (
        'user_id',
        '_displayname',
        'full_name',
    )

    column_searchable_list = \
        column_filters = \
        column_details_list = \
        columns_sortable_list = \
        column_list

    form_columns = ('username', 'full_name')

    column_labels = {
        '_displayname': _('Username'),
    }

    column_formatters = {
        'json_metadata': json_formatter,
    }


user_profile_adminview = {
    'model':     UserProfile,
    'modelview': UserProfileView,
    'category':  _('User Management'),
}

# class MyView(ModelView)
#     def _user_formatter(view, context, model, name):
#         if model.url:
#            markupstring = "<a href='%s'>%s</a>" % (model.url, model.urltitle)
#            return Markup(markupstring)
#         else:
#            return ""

#     column_formatters = {
#         'url': _user_formatter
#     }
