from __future__ import absolute_import, print_function

from invenio_access import action_factory
from invenio_access import Permission
from invenio_access.models import ActionRoles, ActionUsers
from invenio_accounts.models import User
from invenio_db import db
from invenio_access.utils import get_identity 
from flask_principal import PermissionDenied
from functools import partial
from flask_principal import ActionNeed
from invenio_access.permissions import ParameterizedActionNeed
from flask_login import current_user



def iroko_action_factory(name, parameter=False):
    """Factory method for creating new actions (w/wo parameters).

    :param name: Name of the action (prefix with your module name).
    :param parameter: Determines if action should take parameters or not.
        Default is ``False``.
    """
    if parameter:
        return partial(ParameterizedActionNeed, name)
    else:
        return ActionNeed(name)


def is_current_user_source_admin():
    its = False
    try:
        # from sqlalchemy import or_
        # #admin = db.session.query(ActionUsers).filter(ActionUsers.user_id == current_user.id, ActionUsers.exclude == False).filter(or_(ActionUsers.action =="source_full_editor_actions") | (ActionUsers.action=="source_full_gestor_actions")).first() 
        # admin = db.session.query(ActionUsers).filter_by(
        #     user_id=current_user.id, 
        #     exclude=False,
        #     action='source_full_gestor_actions').first() 

        permission = Permission(source_full_gestor_actions)
        current_identity = get_identity(current_user)
        if permission.allows(current_identity):
            its = True

    except Exception as e:        
        print(str(e))
    
    return its


#creando action
source_full_editor_actions = action_factory('source_full_editor_actions')
source_full_gestor_actions = action_factory('source_full_gestor_actions')

ObjectSourceEditor = action_factory('source_editor_actions', parameter=True)
source_editor_actions = ObjectSourceEditor(None)

ObjectSourceGestor = action_factory('source_gestor_actions', parameter=True)
source_gestor_actions = ObjectSourceGestor(None)

ObjectSourceTermGestor = action_factory('source_term_gestor_actions', parameter=True)
source_term_gestor_actions = ObjectSourceTermGestor(None)




def source_editor_permission_factory(obj):
    return Permission(ObjectSourceEditor(obj['uuid']))


def source_gestor_permission_factory(obj):
    try:
        permission = Permission(source_full_gestor_actions)
        current_identity = get_identity(current_user)
        if permission.allows(current_identity):
            return permission
    except Exception as e:
        pass

    return Permission(ObjectSourceGestor(obj['uuid']))


def source_term_gestor_permission_factory(obj):
    if current_user and is_current_user_source_admin():
        return True
    aux = obj['terms']
    terms = aux.split(',')
    permiso = PermissionDenied(ObjectSourceTermGestor(None))

    for term_id in terms:
        try:            
            permiso = Permission(ObjectSourceTermGestor(term_id))
        except Exception as e:
            raise e
    return permiso
         

    


#creando permiso, que requiere varias acciones, por ahora solo la anterior
# source_editor_permission = Permission(source_editor_actions)
# source_gestor_permission = Permission(source_gestor_actions)


#concediendo acceso a un usuario, puede ser por rol
# 1- si es por usuario hay q obtener el usuario, si es por rol igual
# eduardo = db.session.query(User).filter_by(email="eduardo.arencibia@upr.edu.cu").first()
# 2- agregar a la base de datos de access
# db.session.add(ActionUsers.allow(vocabulary_create_permission, user=eduardo))
# db.session.commit()

# #para comprobar, si no es una funcionaldiad q Flask-Security verifique por si mismo, seria asi
# eduardo_identity = get_identity(eduardo)
# permission.allows(eduardo_identity) #Tambie puede ser eduardo_identity.can(permission)


