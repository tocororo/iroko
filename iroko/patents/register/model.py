from invenio_accounts.models import User
from invenio_db import db
from sqlalchemy_utils.types import JSONType, UUIDType

class Register(db.Model):

    __tablename__ = 'iroko_register'

    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    patents = db.Column(db.Integer)

    #instancia del registro
    data = db.Column(JSONType)
