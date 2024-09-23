from flask import Blueprint, flash, jsonify, make_response, request
api_blueprint = Blueprint(
    'iroko_api_graph',
    __name__,
    url_prefix='/graph'
    )
@api_blueprint.route('/pid', methods=['GET'])
def hello():
    return {"hello":"hello"}


