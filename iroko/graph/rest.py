


from __future__ import absolute_import, print_function
from iroko.graph.api import RDFProcessor



from iroko.graph.models import *

from flask import Blueprint, jsonify, request


api_blueprint = Blueprint(
    'iroko_api_graph',
    __name__,
    url_prefix='/graph'
    )
rdf_processor=RDFProcessor()   

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

        if rdf_processor.transform_by_configuration_json(data):
                    return jsonify({'success': 'File uploaded successfully'}), 200

       
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@api_blueprint.route('/sparql', methods=['POST'])
def execute_sparql_query():
    """
    Executes a SPARQL query.
    Returns:
        JSON response indicating success or error.
    """
    try:
        sparql_query = request.form.get('query')
        if not sparql_query:
            return jsonify({'error': 'No SPARQL query provided'}), 400
        
        if not rdf_processor.is_valid_sparql_query(sparql_query):
            return jsonify({'error': 'Invalid SPARQL query'}), 400

        # Call the query method from api.py passing the sparql_query parameter
        results = rdf_processor.execute_sparql_query(sparql_query)
        print("results",results)

        if results:
            return jsonify({'success': 'Query executed successfully', 'results': results}), 200
        else:
            return jsonify({'error': 'Error executing SPARQL query'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
