
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint, current_app, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from iroko.vocabularies.marshmallow import VocabularySchema, TermSchema
from iroko.sources.marshmallow.source import SourceSchema
from iroko.curator.views import blueprint as curator_bp
from iroko.sources.rest import  api_blueprint as sources_bp
import os
from invenio_app.wsgi_rest import application as invenio_rest_app

apispec_blueprint = Blueprint(
    'iroko_apispec',
    __name__,
    url_prefix='/apispec'
)

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

@apispec_blueprint.route('/', methods=['GET'])
def get_apispec():

    spec = APISpec(
        title="Iroko",
        version="-0.3.4",
        openapi_version="3.0.2",
        info=dict(description="Documentation Sceiba API (Iroko)"),
        plugins=[ MarshmallowPlugin(), FlaskPlugin() ]
    )

    exclude = ['invenio_app_ping.ping', 'security.login']

    for url_str, view in invenio_rest_app.view_functions.items():
        if url_str not in exclude:
            spec.path(view=view, app=invenio_rest_app)


    return jsonify(spec.to_dict())


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

