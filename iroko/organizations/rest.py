


from __future__ import absolute_import, print_function

from flask import Blueprint, jsonify, request

from iroko.organizations.api import OrganizationRecord
from iroko.organizations.marshmallow import OrgMetadataSchemaBaseV1, OrgMetadataSchemaRelIDsV1
from iroko.organizations.serializers import json_v1, json_v1_response

api_blueprint = Blueprint(
    'iroko_api_organizations',
    __name__,
    url_prefix='/organizations'
    )


@api_blueprint.route('/pid', methods=['GET'])
def get_org_by_pid_canonical():
    """
    Get a source by any PID received as a argument, including UUID
    this method gives the directed organization with that pid, even if is obsolete or redirected status
    """
    try:
        _id = request.args.get('value')
        print("**********************", _id)
        pid, org = OrganizationRecord.get_org_by_pid(_id)
        if not pid or not org:
            raise Exception('')

        return json_v1_response(pid, org)
        # return jsonify(json_v1.serialize(pid, org))

    except Exception as e:
        return jsonify({
            'ERROR': 'no pid found'.format(_id)
        })


@api_blueprint.route('/notmatterstatus/<pid>', methods=['GET'])
def get_org_by_pid(pid):
    """
    Get a source by any PID received as a argument, including UUID
    this method gives the directed organization with that pid, even if is obsolete or redirected status
    """
    try:
        #_id = request.args.get('value')
        _id = pid
        pid, org = OrganizationRecord.get_org_by_pid(_id)
        if not pid or not org:
            raise Exception('')

        return json_v1_response(pid, org)
        # return jsonify(json_v1.serialize(pid, org))

    except Exception as e:
        return jsonify({
            'ERROR': 'no pid found'.format(_id)
        })


@api_blueprint.route('/active/<pid>', methods=['GET'])
def get_real_org_by_pid(pid):
    """
    Get an active source by any PID received as a argument, including UUID
    If the organization is redirecting other will get the real one is active
    """
    try:
        #_id = request.args.get('value')
        _id = pid
        pid, org = OrganizationRecord.active_org_resolver(_id)
        if not pid or not org:
            raise Exception('')
        print(" === entra a la api active or real org ==", pid)
        return json_v1_response(pid, org)
        # return jsonify(json_v1.serialize(pid, org))

    except Exception as e:
        return jsonify({
            'ERROR': 'No se encontro ninguna organizacion asociada al pid'.format(_id)
        })


organizations_schema_many = OrgMetadataSchemaRelIDsV1(many=True)


def sortOrg(org):
    return org['metadata']['name']


def _get_organization_relationships(uuid, rtype):
    pid, org = OrganizationRecord.get_org_by_pid(uuid)
    if not pid or not org:
        raise Exception('no uuid: {0}'.format(uuid))
    children = []
    for rel in org['relationships']:
        pidvalue = rel['identifiers'][0]['value']
        pid, rel_org = OrganizationRecord.get_org_by_pid(pidvalue)

        if pid and rel_org:
            if rtype:
                if 'type' in rel and rtype == rel['type']:
                    children.append(json_v1.transform_record(pid, rel_org))
            else:
                children.append(json_v1.transform_record(pid, rel_org))
    children.sort(key=sortOrg)
    return children


@api_blueprint.route('/<uuid>/relationships', methods=['GET'])
def get_organization_relationships(uuid):
    """Get a source by any PID received as a argument, including UUID"""
    try:
        rtype = request.args.get('type') if request.args.get('type') else None
        result = _get_organization_relationships(uuid, rtype)
        return jsonify(result)
        # cache = current_cache.get("get_organization_relationships:{0}{1}".format(uuid, rtype)) or {}
        # if "date" not in cache:
        #     cache["date"] = datetime.datetime.now()
        # if datetime.datetime.now() - cache["date"] < datetime.timedelta(days=1) and "stats" in cache:
        #     result = cache["stats"]
        #     return jsonify(result)
        # else:
        #     result = _get_organization_relationships(uuid, rtype)
        #     cache["date"] = datetime.datetime.now()
        #     cache["stats"] = result
        #     current_cache.set("get_organization_relationships:{0}{1}".format(uuid, rtype), cache, timeout=-1)
        #     return jsonify(result)

    except Exception as e:
        return jsonify({
            'ERROR': str(e),
        })


@api_blueprint.route('/<uuid>/curate', methods=['POST'])
#@require_api_auth()
def edit_organization(uuid):
    """
    Dado un uuid modificar los datos de una organizacion, verificando las relaciones que existian y existen
    a partir de esta modificacion que se mantengan consistentemente. Para ello:

    Cuando se edita una org hay que observar:

    Si se agrega una nueva relacion, dichas entidades deben agregarse esa relacion tambien en funcion del tipo
    Si se elimina una relacion, de la misma forma en funcion del tipo

    si la org presente es hija, en la otra seria ver ntre los padres,
    si es padrem entre las hijas,
    en laos demas tipos es en el mismo tipo

    Si se tratan los tipos de relacion como arreglos separados, una modificacion en la relacion entra en eliminar y
    agregar relaciones tambien.

    En el caso de modificar una organizacion hay que tener en cuenta las relaciones previas existentes,
    para detectar las que se eliminan
    """
    try:
        if not request.is_json:
            raise Exception("No se especifican datos en formato json para la curacion")
        input_data = request.json
        print("//////////////////////////////////////////////////////")
        print(input_data)
        print("///////////////////////////////////////////////////////")
        # org = org_json_v1.transform_record(input_data["id"], input_data)
        print("-------------------------------------------------------------")
        # data = OrgMetadataSchemaBaseV1().load(input_data)
        # print(data)

        print("------------------------------------------------------------")

        org, msg = OrganizationRecord.resolve_and_update(input_data["id"], input_data)

        if not org:
            raise Exception("ERROR: ", msg)

        # notification = NotificationSchema()
        # notification.classification = NotificationType.INFO
        # notification.description = _('Nueva fuente ingresada, requiere revisión de un gestor {0}'.format(source.name))
        # notification.emiter = _('Sistema')

        # msg, users = SourcesDeprecated.get_user_ids_source_managers(source.uuid)
        # if users:
        #     for user_id in users:
        #         notification.receiver_id = user_id
        #         Notifications.new_notification(notification)
        #
        # return iroko_json_response(IrokoResponseStatus.SUCCESS, \
        #                            'ok', 'source', \
        #                            {'data': source_schema.dump(source), 'count': 1})
        print("entra ala api de editar organizaciones...........................................")
        return jsonify({
            'SUCCES':"Organizacion modificada",
            'message':msg,
            'org':org
        })
    except Exception as e:
        print(e)
        return jsonify({
            'ERROR': str(e),
        })
