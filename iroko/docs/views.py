from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint, current_app, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
# from sqlalchemy import true

from iroko.organizations.marshmallow import OrgRecordSearchSchemaV1
from iroko.vocabularies.marshmallow import VocabularySchema, TermSchema
from iroko.curator.views import add_vocabulary, add_term
# from iroko.organizations.rest import api_blueprint
from iroko.organizations.rest import api_blueprint, get_org_by_pid
# from iroko.sources.marshmallow.source_v1 import SourceSchemaV1
# from iroko.sources.rest import get_source_by_issn, get_source_by_pid

import os

apispec_blueprint = Blueprint(
    'iroko_apispec',
    __name__,
    url_prefix='/apispec'
)

@apispec_blueprint.route('/', methods=['GET'])
def get_apispec():

    spec = APISpec(
        title="Vocabulary",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(description="Documentation of the Vocabulary module"),
        plugins=[MarshmallowPlugin(), FlaskPlugin()]
    )

    # spec.components.schema(
    #     "Gist",
    #     {
    #         "properties": {
    #             "id": {"type": "integer", "format": "int64"},
    #             "name": {"type": "string"},
    #         }
    #     },
    # )

    spec.components.schema("Vocabulary", schema=VocabularySchema)
    spec.components.schema("Term", schema=TermSchema)

    # spec.path(
    #     path="/gist/{gist_id}",
    #     operations=dict(
    #         get=dict(
    #             responses={"200": {"content": {"application/json": {"schema": "Gist"}}}}
    #         )
    #     ),
    # )

    spec.path(view=add_vocabulary)
    spec.path(view=add_term)

    def add_paths_for_blueprint(spec, blueprint, exclude=()):
        bp_name = blueprint.name
        for url_str, view in current_app.view_functions.items():
            url_paths = url_str.split('.')
            with open('file.txt', 'a') as f:
                if len(url_paths) == 2:
                    prefix, endpoint = url_paths
                    f.write(endpoint + "   " + prefix + "\n")
                    if prefix == bp_name and endpoint not in exclude:
                        spec.path(view=view)


    with current_app.app_context():
        add_paths_for_blueprint(spec, api_blueprint, exclude=('index',))


    # with current_app.test_request_context():
    #     for rule in current_app.url_map.iter_rules():
    #         spec.path(view=current_app.view_functions[rule.endpoint])

    # with current_app.test_request_context():
    #     current_app.register_blueprint(api_blueprint)

    return jsonify(spec.to_dict())

@apispec_blueprint.route('/ex', methods=['GET'])
def get_apispec_ex():

    """Gist detail view.
    ---
    get:
      parameters:
      - in: path
        schema: OrgRecordSearchSchemaV1
      responses:
        200:
          content:
            application/json:
              schema: OrgRecordSearchSchemaV1
    """

    spec = APISpec(
        title="Gist",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(description="A minimal gist API"),
        plugins=[MarshmallowPlugin()]
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

    # spec.components.schema("Organization", schema=OrgRecordSearchSchemaV1)

    spec.path(
        path="/gist/{gist_id}",
        operations=dict(
            get=dict(
                responses={"200": {"content": {"application/json": {"schema": "Gist"}}}}
            )
        ),
    )

    # with current_app.test_request_context():
    #     for rule in current_app.url_map.iter_rules():
    #         spec.path(view=current_app.view_functions[rule.endpoint])

    # with current_app.test_request_context():
    #     current_app.register_blueprint(api_blueprint)

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

