import json

from flask.json import jsonify
from invenio_search import RecordsSearch
from rdflib import RDF, RDFS, Graph

from iroko.graph.mapping_to_rdf.configuration_manager import ConfigurationManager
from iroko.graph.mapping_to_rdf.create_graph import Create_Graph
from iroko.graph.mapping_to_rdf.mapping_to_rdf import MappingtoRDF
from iroko.organizations.search import OrganizationSearch
from iroko.sources.search import SourceSearch

namespaces = {
        
        "sceiba":"http//sceiba.org"
    }

def transform_by_configuration_json(configuration_json):
    graph=Create_Graph()
    graph.add_namespaces(namespaces)


    try:
        data_dict = json.loads(configuration_json)
        configuration_manager = ConfigurationManager(data_dict, "sceiba")
        if configuration_manager.validate_config_json():
            for entity in configuration_manager.put_the_order():
                   entitysearch_by_name=get_entitysearch_by_name(entity.get("name"))
                   if entitysearch_by_name:
                      mapping = MappingtoRDF(graph, configuration_manager,
                                           get_and_save_by_search_class(entitysearch_by_name),
                                             entity.get("name"))
                      

                      graph.graph.parse=graph.graph+ mapping._mapping_entity()

                   else:
                      print("no se encuentra")
                      continue

            print("graph====",graph.serialize(format="ttl"))

        else:
            return False
    except:
        return False
    
    return True

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