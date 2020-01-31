from typing import Dict
from flask_babelex import lazy_gettext as _
from invenio_db import db
from invenio_access.utils import get_identity 
from flask_login import current_user
from iroko.sources.models import TermSources
from flask_babelex import lazy_gettext as _
from marshmallow import ValidationError
from invenio_access import Permission
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User


class Issn:
    '''Manage Issn'''

    @classmethod
    def get_issn(cls, issn) -> Dict[str, dict]:

        issn_text = open('/home/reinier/Escritorio/issn.info.json','w')
        print(issn_text)
        issn = {}

        if issn:
            return 'ok', issn
        else:
            msg = 'Issn not exist name={0}'.format(issn)
            return msg, None
