
#  This file is part of SCEIBA.
#  Copyright (c) 2020. UPR
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

"""Iroko sources api views."""

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template
from flask_login import login_required

from .forms import FaqForm


blueprint = Blueprint(
    'iroko_texts',
    __name__,
    url_prefix='/texts',
    template_folder='templates'
)


@blueprint.route('/faqs')
@login_required
def edit_faq(id=None):
    # security questiong here
    # print(current_user.has_role('curator'))

    form = FaqForm()

    return render_template('edit_faq.html', form=form)
