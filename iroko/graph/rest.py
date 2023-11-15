


from __future__ import absolute_import, print_function


from iroko.graph.api import transform_by_configuration_json

from iroko.graph.models import *

from flask import Blueprint, jsonify, request


api_blueprint = Blueprint(
    'iroko_api_graph',
    __name__,
    url_prefix='/graph'
    )

@api_blueprint.route('/config', methods=['POST'])
def upload_configuration_file():
    """
    Uploads a configuration file.

    Returns:
        JSON response indicating success or error.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file attached'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file and file.filename.endswith('.json'):
        data = file.read()
        if transform_by_configuration_json(data):
                    return jsonify({'success': 'File uploaded successfully'}), 200

       
    else:
        return jsonify({'error': 'Invalid file type'}), 400

