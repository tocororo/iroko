# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# Iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Records API."""

from __future__ import absolute_import, print_function

import enum
import traceback
from copy import deepcopy
from uuid import uuid4

from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_jsonschemas import current_jsonschemas
from invenio_pidstore.errors import PIDDoesNotExistError, PIDDeletedError
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_pidstore.resolver import Resolver
from invenio_records_files.api import Record
from sqlalchemy.orm.exc import NoResultFound

from iroko.api import IrokoBaseRecord
from iroko.pidstore import pids
from iroko.pidstore.pids import (
    ORGANIZATION_PID_TYPE, IROKO_OBJECT_TYPE, IDENTIFIERS_FIELD,
    identifiers_schemas, IDENTIFIERS_FIELD_TYPE, IDENTIFIERS_FIELD_VALUE,
    )
# TODO: cuando se actualiza una organizacion y se pone status: "redirected"
#  no aparece la informacion de a cual redirecciona.... incluir esto...


class IrokoResponseStatus(enum.Enum):
    PARENT = "parent"
    CHILD = "child"
    RELATED = "related"
    other = "other"


class OrganizationRecord(IrokoBaseRecord):
    """Custom record."""

    _schema = "organizations/organization-v1.0.0.json"

    @classmethod
    def create_or_update(cls, org_uuid, data, **kwargs):
        """Create or update OrganizationRecord."""

        # assert org_uuid
        org, msg = cls.resolve_and_update(org_uuid, data)
        # if resolve_and_update do no return, then is not existed org, so trying to create one
        if not org:
            print("no pids found, creating organization")
            created_org = cls.create(data, iroko_pid_type=pids.ORGANIZATION_PID_TYPE,
                          iroko_pid_value=org_uuid)
            org = created_org
            msg = 'created'

        return org, msg


    def update(self, data):
        """Update data for record."""
        self.update_relationships(data)
        super(OrganizationRecord, self).update_record(data)

        return self


    @classmethod
    def get_org_by_pid(cls, pid_value, with_deleted=False):
        resolver = Resolver(
            pid_type=ORGANIZATION_PID_TYPE,
            object_type=IROKO_OBJECT_TYPE,
            getter=cls.get_record,
            )
        try:
            return resolver.resolve(str(pid_value))
        except Exception:
            pass

        for pid_type in identifiers_schemas:
            try:
                resolver.pid_type = pid_type
                schemapid, org = resolver.resolve(pid_value)
                pid = PersistentIdentifier.get(ORGANIZATION_PID_TYPE, org['id'])
                return pid, org
            except Exception as e:
                pass
        return None, None

    @classmethod
    def active_org_resolver(cls, pid_value, with_deleted=False):
        """
        Este metodo es en esencia muy similar a get_org_by_pid, primeramente obtiene el objeto org
        usando cualquiera de los identificadores como filtro de busqueda,
        pero adicionalmente comprueba que el estado de la org resultante es activo, si fuere
        redirected
        pues la org que devuelve es dicha org apunta,
        en caso de que no tenga registrado en el campo redirected a quien apunta emite Error
        en caso que se solicita una org cuyo estado es obsolete emite error 400
        """
        try:
            pid, org = cls.get_org_by_pid(pid_value, with_deleted)
            if (org["status"] == "redirected"):
                if ("redirect" not in org):
                    raise Exception(
                        "No se han especificados los datos de la organizacion a quien redirecciona."
                        )

                real_org_pid = org["redirect"]["value"]
                pid, org = cls.active_org_resolver(real_org_pid, with_deleted)

            return pid, org
        except Exception as e:
            print("error> ", str(e))
            pass
        return None, None

    @classmethod
    def check_organization_before_crud(cls, uuid, data, adding=False, on_demand=False):
        """
        Este metodo debe ser capaz de revisar las cuestiones de reglas de negocios para la adicion
        y para la modificacion de metadatos de la organizacion
        param data es el json de la org
        param adding dice si esta en la accion de adicionar o de editar
        La estructura del json no hay q validarla, eso lo hace el metodo commit.

        debe verificar si es adicionar:
        si es cubana que no tenga incluido entre los datos q se quieren adicionar reup,
        ni orgaid, ni uniid
        (estos datos solo se toman desde la ONEI)
        debe tener como parent alguna org con reup, no se permite adicionar org de primer nivel

        debe verificar cuando modifica que no cambia el reup si existe

        """

        return True

    def get_relationships(self):
        if not 'relationships' in self:
            self['relationships'] = []
        return self['relationships']

    def set_relationships(self, rel):
        self['relationships'] = rel

    relationships = property(get_relationships, set_relationships)

    def update_relationships(self, data):
        """Este metodo busca las relaciones que hay que adicionar o eliminar en las
        organizaciones relacionadas y las elimina. Ejemplo:
        self = {
            name: 'UH',
            relationships: {
                {name: MES, type: parent},
                {name: MATCOM, type: child},
                {name: DICT, type: child},
                {name: JARDIN, type: child},
            }
        data = {
            name: 'UH',
            relationships: {
                {name: MES, type: parent},
                {name: DICT, type: child},
                {name: JARDIN, type: child},
                {name: FCOM, type: child},
            }
        Como resultado de la ejecución de este método:
        - en la organización MATCOM se elimina la relación parent con UH
        - en la organización FCOM se adiciona la relación parent con UH
        """
        org = self

        if 'relationships' not in org:
            org["relationships"] = []
        if 'relationships' not in data:
            data["relationships"] = []
        old_relationships = list(org["relationships"])
        new_relationships = list(data["relationships"])

        for old_item in org["relationships"]:
            exist = False
            # no usar lista.remove porque puede haber diferencia en el campo identifiers y
            # sea la misma org
            old_aux = new_aux = None
            for new_item in data["relationships"]:
                if "id" in old_item:
                    old_aux = old_item["id"]
                if "id" in new_item:
                    new_aux = new_item["id"]
                # tuve q usar estos aux porque hay errores en los datos de la base de datos
                # en el campop relationships
                # no esta el id en ocasiones
                if 'type' not in old_item:
                    old_item["type"] = 'other'
                if 'type' not in new_item:
                    new_item["type"] = 'other'
                if old_aux and new_aux and old_aux == new_aux and old_item["type"] == new_item[
                    "type"]:
                    exist = True
                    new_relationships.remove(new_item)
                    old_relationships.remove(old_item)
                    # si existe en las relaciones que ya tenia, no interesa si la nueva viene
                    # con mas pids
                    # el final esta y por el uuid se recupera, pero si cambia el tipo de
                    # relacion
                    # se agrega como una nueva, eliminando la anterior que es la misma org
                    # pero con diferente tipo
                    break
        actual = {
            "id": data["id"],
            "identifiers": data["identifiers"],
            "label": data["name"]
            }
        print("actuallllllllllllllllllllllllllllll")
        print(actual)
        print("````````````````````````````````````")
        self.delete_relationships_in_related(old_relationships)
        self.add_relationships_in_related(new_relationships, actual)

    def add_relationships_in_related(self, relationships, self_rel=None):
        """adiciona la relacion self en las organizaciones relacionadas"""
        if not self_rel:
            self_rel = {
                'id': self.iroko_uuid,
                'identifiers': self.identifiers,
                'name': self.get_field('name')
                }
        for relation in relationships:
            pid_value = None
            if "id" in relation:
                pid_value = relation["id"]
            elif "identifiers" in relation and len(relation["identifiers"]) > 0:
                pid_value = relation["identifiers"][0]["value"]
            if pid_value:
                org = OrganizationRecord.get_record_by_pid_value(pid_value)
                if org:
                    org.add_relation(self_rel)

    def delete_relationships_in_related(self, relationships):
        """Elimina la relacion de self en las organizaciones relacionadas."""
        for relation in relationships:
            pid_value = None
            if "id" in relation:
                pid_value = relation["id"]
            elif "identifiers" in relation and len(relation["identifiers"]) > 0:
                pid_value = relation["identifiers"][0]["value"]
            if pid_value:
                org = OrganizationRecord.get_record_by_pid_value(pid_value)
                if org:
                    org.remove_relation(self.iroko_uuid)

    def add_relation(self, relation, update_record=True):
        """add a relation, if relation['id'] already exists, then update
        if update_record==True, then call base update record.
        """
        self.add_update_item_to_list_field('relationships', 'id', relation)
        if update_record:
            self.update_record()

    def remove_relation(self, pid, update_record=True):
        """Remove a relation. Search for pid in id field or identifiers field"""
        new_relationships = []
        remove = False
        for rel in self.relationships:
            if 'id' in rel and rel['id'] == pid:
                remove = True
            if 'identifiers' in rel:
                for _pid in rel['identifiers']:
                    if pid == _pid['value']:
                        remove = True
            if not remove:
                new_relationships.append(rel)
        self.relationships =  new_relationships
        if update_record:
            self.update_record()

    def is_from(self, country_name='Cuba', country_code='cu'):
        """
        return true is one address has the input country_name or country_code
        """
        if 'addresses' in self:
            for address in self['addresses']:
                if ('country' in address and address['country'] == 'Cuba') or (
                    'country_code' in address and address['country_code'] == 'cu'):
                    return True
        return False

    def has_identifiers(self, id_schemas, has_any=True):
        """return true .
        id_schemas: a list of identifiers schemas
        if has_any==True, return true if the organization has any of the id_schemas
        if has_any==False, return true if the organization has all the id_schemas"""
        if not 'identifiers' in self:
            return False
        if has_any:
            for ide in self['identifiers']:
                for schema in id_schemas:
                    if ide[IDENTIFIERS_FIELD_TYPE] == schema:
                        return True
            return False
        else:
            sc = len(id_schemas)
            i = 0
            for ide in self['identifiers']:
                for schema in id_schemas:
                    if ide[IDENTIFIERS_FIELD_TYPE] == schema:
                        i = i + 1
            return sc == i

    def deleting_relations(self, old_relations, actual):
        """
        param lost_relations tiene los elementos del campo relationships que ya no estaran mas en
        la org,
        la idea es recorrer cada una de estas orgs e informarles que ya no tienen relacion,
        param actual ofrece un dict q solo falta el type de relation para que pueda ser usado al
        encontrar indice
        param resolver es capaz de resolver dado un uuid la organizacion
        """

        for relation in old_relations:
            pid_value = None
            if "id" in relation:
                pid_value = relation["id"]
            elif "identifiers" in relation and len(relation["identifiers"]) > 0:
                pid_value = relation["identifiers"][0]["value"]

            # hice esto anterior por errores en los datos en la base de datos
            persistent_identifier, org = OrganizationRecord.get_org_by_pid(pid_value)
            if org:
                print("--------------deleting relationships--------------------------")
                if relation["type"] == "parent":
                    actual["type"] = "child"
                elif relation["type"] == "child":
                    actual["type"] = "parent"
                else:
                    actual["type"] = relation["type"]
                print(actual)

                rels = org["relationships"]
                try:
                    rels.remove(actual)
                    org.commit()
                except ValueError:
                    print("ValueError, porque no esta en la lista de relaciones")
                    pass
                print(org)
                print("-----------------------------------------------------------------")
                # .update(data, dbcommit=dbcommit, reindex=reindex)

    def adding_relations(self, new_relations, actual):
        """
        param new_relations nuevas orgs con las que tendra actual relacion,
        debe informarse a cada una de su nueva relacion
        param actual ofrece un dict q solo falta el type de relation para que pueda ser usado al
        encontrar indice
        """

        for relation in new_relations:
            pid = ""
            if "id" in relation:
                pid = relation["id"]
            elif "identifiers" in relation and len(relation["identifiers"]) > 0:
                pid = relation["identifiers"][0]["value"]
            # hice esto anterior por errores en los datos en la base de datos
            persistent_identifier, org = OrganizationRecord.get_org_by_pid(pid)

            if org:
                print("--------------adding relationships--------------------------")
                print(org)
                print("===============")
                print("===============")
                print(relation)
                print("===============")
                print("===============")
                # print("{0}={1} found".format(org["name"], relation["id"]))
                if relation["type"] == "parent":
                    actual["type"] = "child"
                elif relation["type"] == "child":
                    actual["type"] = "parent"
                else:
                    actual["type"] = relation["type"]
                print(actual)

                org["relationships"].append(actual)
                print(org)
                print("-----------------------------------------------------------------")
                org.commit()
                # .update(data, dbcommit=dbcommit, reindex=reindex)

#5148
