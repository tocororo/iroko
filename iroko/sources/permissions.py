#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from __future__ import absolute_import, print_function

from functools import partial

from flask_login import current_user
from flask_principal import PermissionDenied, ActionNeed
from invenio_access import action_factory, Permission
from invenio_access.models import ActionUsers
from invenio_access.permissions import ParameterizedActionNeed
from invenio_access.utils import get_identity
from invenio_accounts.models import User
from invenio_db import db


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


# LA LOGICA DE LOS PERMISOS ES LA SIGUIENTE:
# 1- source_full_manager_actions: se le asigna a un usuario
#   significa que el usuario es administrador de todas las fuentes.
#   un usuario administrador(manager) de fuentes puede cambiar el campo source_status

# 2- source_editor_actions: se le asigna a un usuario para un SourceRecord.id:
#   significa que el usuario puede crear versiones de ese SourceRecord

# 3- source_term_manager_actions: se le asigna a un usuario para un Term.id:
#   significa que todas las SourcesRecord que tengan en el campo classifications.id ese Term.id
#   son administradas por el usuario.

# 4- source_organization_manager_actions: se le asigna a un usuario para un Organization.id:
#   significa que todas las SourcesRecord que tengan en el campo organizations.id ese Organization.id
#   son administradas por el usuario.


# creando action
source_full_manager_actions = action_factory('source_full_manager_actions')

ObjectSourceEditor = action_factory('source_editor_actions', parameter=True)
source_editor_actions = ObjectSourceEditor(None)

ObjectSourceManager = action_factory('source_manager_actions', parameter=True)
source_manager_actions = ObjectSourceManager(None)
# TODO: Eliminar este permiso, no tiene sentido

ObjectSourceTermManager = action_factory('source_term_manager_actions', parameter=True)
source_term_manager_actions = ObjectSourceTermManager(None)

ObjectSourceOrganizationManager = action_factory('source_organization_manager_actions', parameter=True)
source_organization_manager_actions = ObjectSourceOrganizationManager(None)


def is_user_sources_admin(user: User):
    its = False
    permission = Permission(source_full_manager_actions)
    current_identity = get_identity(user)
    if permission.allows(current_identity):
        its = True

    # except Exception as e:
    #     # print(str(e))

    return its


def user_is_organization_manager(uuid, user: User):
    if not user or not uuid:
        raise PermissionDenied()
    identity = get_identity(user)
    permission = Permission(ObjectSourceOrganizationManager(uuid))
    if permission.allows(identity):
        return True
    raise PermissionDenied()


def user_is_term_manager(uuid, user: User):
    if not user or not uuid:
        raise PermissionDenied()
    identity = get_identity(user)
    permission = Permission(ObjectSourceTermManager(uuid))
    if permission.allows(identity):
        return True
    raise PermissionDenied()


def user_has_manager_permission(source, user: User):
    if not user or not source:
        raise PermissionDenied()

    identity = get_identity(user)

    permission = Permission(source_full_manager_actions)
    if permission.allows(identity):
        return True

    permiso = Permission(ObjectSourceManager(source.id))
    if permiso.allows(identity):
        return True

    if 'classifications' in source.model.json:
        for term in source.model.json['classifications']:
            if 'id' in term:
                try:
                    permiso = Permission(ObjectSourceTermManager(term['id']))
                    if permiso.allows(identity):
                        return True
                except Exception as e:
                    pass

    if 'organizations' in source.model.json:
        for org in source.model.json['organizations']:
            if 'id' in org:
                try:
                    permiso = Permission(ObjectSourceOrganizationManager(org['id']))
                    if permiso.allows(identity):
                        return True
                except Exception as e:
                    pass

    raise PermissionDenied()


def user_has_edit_permission(source, user: User):
    if not user or not source:
        raise PermissionDenied()
    try:
        if user_has_manager_permission(source, user):
            return True
    except PermissionDenied as err:
        pass

    identity = get_identity(user)
    perm = Permission(ObjectSourceEditor(source.id))
    if perm.allows(identity):
        return True
    raise PermissionDenied()


def source_editor_permission_factory(obj):
    return Permission(ObjectSourceEditor(obj['uuid']))


def source_manager_permission_factory(obj):
    try:
        permission = Permission(source_full_manager_actions)
        current_identity = get_identity(current_user)
        if permission.allows(current_identity):
            return permission
    except Exception as e:
        pass

    return Permission(ObjectSourceManager(obj['uuid']))


def source_term_manager_permission_factory(obj):
    permission = Permission(source_full_manager_actions)
    current_identity = get_identity(current_user)
    if permission.allows(current_identity):
        return permission

    permiso = None
    permiso = Permission(ObjectSourceManager(obj['uuid']))
    if permiso:
        return permiso

    aux = obj['terms']
    terms = aux.split(',')
    permiso = None

    for term_uuid in terms:
        try:
            permiso = Permission(ObjectSourceTermManager(term_uuid))
            if permiso:
                return permiso
        except Exception as e:
            raise e
    raise PermissionDenied('No tiene permisos de gestión')


def source_organization_manager_permission_factory(obj):
    permission = Permission(source_full_manager_actions)
    current_identity = get_identity(current_user)
    if permission.allows(current_identity):
        return permission

    permiso = None
    permiso = Permission(ObjectSourceManager(obj['uuid']))
    if permiso:
        return permiso

    aux = obj['orgs']
    orgs = aux.split(',')
    permiso = None

    for org_uuid in orgs:
        try:
            permiso = Permission(ObjectSourceOrganizationManager(org_uuid))
            if permiso:
                return permiso
        except Exception as e:
            raise e
    raise PermissionDenied('No tiene permisos de gestión')


def user_has_editor_or_manager_permissions(obj):
    permission = Permission(source_full_manager_actions)
    current_identity = get_identity(current_user)
    if permission.allows(current_identity):
        return permission

    permiso = None
    permiso = Permission(ObjectSourceManager(obj['uuid']))
    if permiso:
        return permiso

    aux = obj['terms']
    terms = aux.split(',')
    permiso = None
    for term_uuid in terms:
        try:
            permiso = Permission(ObjectSourceTermManager(term_uuid))
            if permiso:
                return permiso
        except Exception as e:
            raise e

    aux = obj['orgs']
    orgs = aux.split(',')
    permiso = None
    for org_uuid in orgs:
        try:
            permiso = Permission(ObjectSourceTermManager(org_uuid))
            if permiso:
                return permiso
        except Exception as e:
            raise e
    return Permission(ObjectSourceEditor(obj['uuid']))


def get_arguments_for_source_from_action(puser, paction):
    arguments = list(map(lambda x: x.argument,
                         db.session.query(ActionUsers).filter_by(user=puser, exclude=False, action=paction).all()))

    return arguments


def get_user_ids_for_source_from_action(paction, p_argument=None):
    if p_argument:
        user_ids = list(map(lambda x: x.user.id,
                            db.session.query(ActionUsers).filter_by(argument=str(p_argument), exclude=False,
                                                                    action=paction).all()))
    else:
        user_ids = list(
            map(lambda x: x.user.id, db.session.query(ActionUsers).filter_by(exclude=False, action=paction).all()))

    return user_ids


def check_source_status(record, *args, **kwargs):
    """Return permission that check if the record exists in ES index.

    :params record: A record object.
    :returns: A object instance with a ``can()`` method.
    """

    def can(self):
        """Try to search for given record."""
        return record['source_status'] == 'APPROVED'

    return type('CheckStatus', (), {'can': can})()

# creando permiso, que requiere varias acciones, por ahora solo la anterior
# source_editor_permission = Permission(source_editor_actions)
# source_manager_permission = Permission(source_manager_actions)


# concediendo acceso a un usuario, puede ser por rol
# 1- si es por usuario hay q obtener el usuario, si es por rol igual
# eduardo = db.session.query(User).filter_by(email="eduardo.arencibia@upr.edu.cu").first()
# 2- agregar a la base de datos de access
# db.session.add(ActionUsers.allow(vocabulary_create_permission, user=eduardo))
# db.session.commit()

# #para comprobar, si no es una funcionaldiad q Flask-Security verifique por si mismo, seria asi
# eduardo_identity = get_identity(eduardo)
# permission.allows(eduardo_identity) #Tambie puede ser eduardo_identity.can(permission)
