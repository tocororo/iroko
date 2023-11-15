import json

from flask.json import jsonify
from invenio_search import RecordsSearch
from rdflib import RDF, RDFS, Graph
import rdflib
from rdflib.plugins.sparql.parser import parseQuery

from iroko.graph.mapping_to_rdf.configuration_manager import ConfigurationManager
from iroko.graph.mapping_to_rdf.create_graph import Create_Graph
from iroko.graph.mapping_to_rdf.mapping_to_rdf import MappingtoRDF
from iroko.organizations.search import OrganizationSearch
from iroko.sources.search import SourceSearch

namespaces = {
        
        "sceiba":"http//sceiba.org"
    }
global general_grap

general_grap=Graph()

def transform_by_configuration_json(configuration_json):
    create_graph=Create_Graph()
    create_graph.add_namespaces(namespaces)


    try:
        data_dict = json.loads(configuration_json)
        configuration_manager = ConfigurationManager(data_dict, "sceiba")
        if configuration_manager.validate_config_json():
            for entity in configuration_manager.put_the_order():
                   entitysearch_by_name=get_entitysearch_by_name(entity.get("name"))
                   if entitysearch_by_name:
                      mapping = MappingtoRDF(create_graph, configuration_manager,
                                           get_and_save_by_search_class(entitysearch_by_name),
                                             entity.get("name"))
                      create_graph.graph=create_graph.graph+ mapping._mapping_entity()
                   else:
                      print("no se encuentra")
                      continue
            #print("graph====",graph.serialize(format="ntriples"))
            general_grap=create_graph.graph
  
        else:
            return False
    except:
        return False
    
    return True
def query(sparql_query):
    print(general_grap.serialize(format="ntriples"))
    try:
        # Set the graph to query
        

        knows_query =  """SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o
  FILTER (?o = "active")
}"""
        # Execute the SPARQL query

        qres = general_grap.query(knows_query)
        results = []
        for row in qres:
        # Process each row of the query results
          print("row",row)
        
        return results
    except Exception as e:
        print(f"An error occurred during the query: {str(e)}")
        return None
def is_valid_sparql_query(query):
    try:
        parseQuery(query)
        return True
    except Exception:
        return False

def get_entitysearch_by_name(name: str):
    """   

    Get the entity search object based on the given name.

    Args:
        name (str): Name of the entity.

    Returns:
        EntitySearch: Entity search object.

    Raises:
        ValueError: If the given name is not valid.
    """
    if name == "Organizations":
        return OrganizationSearch()
    elif name == "Sources":
        return SourceSearch()
    elif name == "Records":
        return RecordsSearch()
    
def get_and_save_by_search_class(search_class):
    total_item = search_class
    offset = 0
    instances = []

    for item in total_item.scan():
       instances.append(item.to_dict())
       offset += 1
       "hecho para que solo guarde 5 instancias ,despues se quitara"
       if offset==5:
          break
          
    
    # Guardar las instancias en un archivo JSON
    with open('instances.json', 'w') as file:
        json.dump(instances, file)
        print(f"Guardadas {offset} instancias de {search_class}")

    print("Proceso completado")
    return instances     