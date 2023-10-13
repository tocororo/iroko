from apispec import APISpec
# from apispec.ext.marshmallow import MarshmallowPlugin
# from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint, current_app, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
# from sqlalchemy import true

# from iroko.organizations.marshmallow import OrgRecordSearchSchemaV1
# from iroko.sources.marshmallow.source_v1 import SourceSchemaV1
# from iroko.sources.rest import get_source_by_issn, get_source_by_pid

apispec_blueprint = Blueprint(
    'iroko_apispec',
    __name__,
    url_prefix='/apispec'
)

@apispec_blueprint.route('/', methods=['GET'])
def get_apispec():

    spec = APISpec(
        title="Gist",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(description="A minimal gist API"),
    )

    spec.components.schema(
        "Gist",
        {
            "properties": {
                "id": {"type": "integer", "format": "int64"},
                "name": {"type": "string"},
            }
        },
    )

    spec.path(
        path="/gist/{gist_id}",
        operations=dict(
            get=dict(
                responses={"200": {"content": {"application/json": {"schema": "Gist"}}}}
            )
        ),
    )

    return jsonify(spec.to_dict())


# @apispec_blueprint.route('/', methods=['GET'])
# def get_apispec():
#     spec = APISpec(
#         title="Iroko",
#         version="0.3.4",
#         openapi_version="3.0.2",
#         info=dict(description="Iroko API Docs"),
#         plugins=[FlaskPlugin(), MarshmallowPlugin()],
#         servers=[dict(url="/api")]
#     )
#     uuid = {
#           "name": "uuid",
#           "in": "path",
#           "required": true,
#           "description": "UUID of the source that we want to match",
#           "type": "string"
#         }
#     ops = {
#         "get": {
#         "tags": [
#           "Sources"
#         ],
#         "summary": "Return a Source",
#         "responses": {
#           "200": {
#             "description": "OK",
#             "schema": {
#               "$ref": "#/components/schemas/sources"
#             }
#           },
#           "400": {
#             "description": "Failed. Misunderstood Request."
#           },
#           "404": {
#             "description": "Failed. Source request not found."
#           }
#         }
#       }
#     }
#     # spec.path(path='/pid/source/{uuid}', parameters=[uuid], operations=ops)
#     spec.path(view=get_source_by_issn, app=current_app).path(view=get_source_by_pid, app=current_app)
#     spec.components.schema("sources", schema=SourceSchemaV1).\
#         schema("organizations", schema=OrgRecordSearchSchemaV1)

#     return jsonify(spec.to_dict())



### docs specific ###
SWAGGER_URL = '/apidocs'
API_URL = '/apispec'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Iroko API Docs"
    }
)



