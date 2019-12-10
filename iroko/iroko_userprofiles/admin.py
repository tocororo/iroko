from invenio_userprofiles.admin import UserProfileView
from .models import IrokoUserProfile
from flask_babelex import lazy_gettext as _


class IrokoUserProfileView(UserProfileView):
    """Userprofiles view. Links User ID to user profile."""

    column_list = (
        'user_id',
        '_displayname',
        'full_name',
        'extra',
    )

    column_searchable_list = \
        column_filters = \
        column_details_list = \
        columns_sortable_list = \
        column_list

    form_columns = ('username', 'full_name', 'extra')

    column_labels = {
        '_displayname': ('Username'),
    }


user_profile_adminview = {
    'model': IrokoUserProfile,
    'modelview': IrokoUserProfileView,
    'category': _('User Management'),
}