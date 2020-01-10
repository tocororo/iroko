from invenio_access import action_factory
from invenio_access import Permission
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 


#creando action
source_editor_actions = action_factory('source_editor_actions', parameter=True)
source_gestor_actions = action_factory('source_gestor_actions', parameter=True)

#creando permiso, que requiere varias acciones, por ahora solo la anterior
source_editor_permission = Permission(source_editor_actions)
source_gestor_permission = Permission(source_gestor_actions)


#concediendo acceso a un usuario, puede ser por rol
# 1- si es por usuario hay q obtener el usuario, si es por rol igual
# eduardo = db.session.query(User).filter_by(email="eduardo.arencibia@upr.edu.cu").first()
# 2- agregar a la base de datos de access
# db.session.add(ActionUsers.allow(vocabulary_create_permission, user=eduardo))
# db.session.commit()

# #para comprobar, si no es una funcionaldiad q Flask-Security verifique por si mismo, seria asi
# eduardo_identity = get_identity(eduardo)
# permission.allows(eduardo_identity) #Tambie puede ser eduardo_identity.can(permission)


def grant_source_editor_permission(user, source):
    try:        
        db.session.add(ActionUsers.allow(source_editor_actions(source.id, user=user)))
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
        return False


def deny_source_editor_permission(user, source):
    try:
        db.session.add(ActionUsers.deny(source_editor_actions(source.id, user=user)))
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
        return False


def check_user_source_editor_permission(user, source):
    try:
        user_identity = get_identity(user)
        permission = Permission(source_editor_actions(source.id))
        return permission.allows(user_identity)
    except Exception as e:
        print(str(e))
        return False