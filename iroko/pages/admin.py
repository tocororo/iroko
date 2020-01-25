from flask_admin.contrib.sqla import ModelView

#from iroko.pages.models import Faq


# class FaqModelView(ModelView):
#     """View for managing vocabularies."""

#     # can_view_details = True

#     list_all = ('id', 'question', 'answer')

#     column_list = list_all

#     column_default_sort = ('question', True)

#     column_filters = ('question')

#     form_columns = ('question', 'answer')



# faq_adminview = dict(
#     modelview=FaqModelView,
#     model=Faq,
#     name='FAQ',
#     category='Iroko'
# )



# __all__ = ('faq_adminview')