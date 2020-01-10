from invenio_access import action_factory
from invenio_access import Permission
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 


#creando action
create_source_curator = action_factory('curator-source-add')
create_vocabulary_curator = action_factory('curator-vocabulary-add')

#creando permiso, que requiere varias acciones, por ahora solo la anterior
source_create_permission = Permission(create_source_curator)
vocabulary_create_permission = Permission(create_vocabulary_curator)


#concediendo acceso a un usuario, puede ser por rol
# 1- si es por usuario hay q obtener el usuario, si es por rol igual
# eduardo = db.session.query(User).filter_by(email="eduardo.arencibia@upr.edu.cu").first()
# 2- agregar a la base de datos de access
# db.session.add(ActionUsers.allow(vocabulary_create_permission, user=eduardo))
# db.session.commit()

# #para comprobar, si no es una funcionaldiad q Flask-Security verifique por si mismo, seria asi
# eduardo_identity = get_identity(eduardo)
# permission.allows(eduardo_identity) #Tambie puede ser eduardo_identity.can(permission)