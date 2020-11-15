"""Iroko Admin views."""

from flask_admin.contrib.sqla import ModelView

from .models import Vocabulary, Term


class VocabularyModelView(ModelView):
    """View for managing vocabularies."""

    # can_view_details = True

    list_all = ('id', 'identifier', 'human_name', 'description')

    column_list = list_all

    column_default_sort = ('id', True)

    column_filters = list_all

    form_columns = ('identifier', 'human_name', 'description')


class TermModelView(ModelView):
    """View for managing terms."""

    # can_view_details = True

    list_all = ('id', 'identifier', 'description', 'vocabulary', 'uuid')

    column_list = list_all

    column_default_sort = ('identifier', True)

    column_filters = ('id', 'uuid', 'identifier', 'vocabulary')

    # form_columns = ('name', 'description')
    form_columns = ('vocabulary', 'identifier', 'description', 'parent_id')


vocabularies_adminview = dict(
    modelview=VocabularyModelView,
    model=Vocabulary,
    name='Vocabularies',
    category='Iroko'
)

terms_adminview = dict(
    modelview=TermModelView,
    model=Term,
    name='Terms',
    category='Iroko'
)

__all__ = ('vocabularies_adminview', 'terms_adminview')
