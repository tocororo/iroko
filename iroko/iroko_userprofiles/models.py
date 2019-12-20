from invenio_db import db
from invenio_userprofiles.models import UserProfile


class IrokoUserProfile(UserProfile):
    """
    Hereda de user profile para agregar campos propios del sistema como extra
    """
    __tablename__ = 'iroko_userprofiles_userprofile'

    extra = db.Column('extra', db.String(250), unique=False, nullable=False, default='')
    """Lower-case version of username to assert uniqueness."""
