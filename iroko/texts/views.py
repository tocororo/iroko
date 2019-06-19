
"""Iroko sources api views."""

from __future__ import absolute_import, print_function
from flask import Blueprint, request, render_template, flash, url_for, redirect
from flask_login import login_required
from flask_babelex import lazy_gettext as _
from os import listdir, path
from .forms import FaqForm
import uuid
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user


blueprint = Blueprint(
    'iroko_texts',
    __name__,
    url_prefix='/texts',    
    template_folder='templates'   
)


@blueprint.route('/faqs')
@login_required
def edit_faq(id=None):    
    #security questiong here
    print(current_user.has_role('curator'))
    
    form = FaqForm()
   
    return render_template('edit_faq.html', form=form)

