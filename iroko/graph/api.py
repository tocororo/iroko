import json

from invenio_search import RecordsSearch
from rdflib import Graph
from rdflib.plugins.sparql.parser import parseQuery

from iroko.api import IrokoRecordIterator
from iroko.graph.rdf.configuration_manager import ConfigurationManager
from iroko.graph.rdf.creategraph import CreateGraph
from iroko.graph.rdf.mapping_to_rdf import RDFMapper
from iroko.organizations.search import OrganizationSearch
from iroko.sources.search import SourceSearch


class RDFProcessor:
    def __init__(self):
        self.namespaces = {
            "sceiba": "http//sceiba.cu/"
            }
        self.general_graph = Graph()

    def transform_by_configuration_json(self, configuration_json):
        """    Transform data based on the provided configuration JSON.


        Args:
        configuration_json (dict): The configuration JSON specifying the transformation rules.

        Returns:
        dict: The transformed data.
        """
        create_graph = CreateGraph()
        create_graph.graph = create_graph.add_namespaces(self.namespaces)
        # try:
        data_dict = json.loads(configuration_json)
        configuration_manager = ConfigurationManager(data_dict, "sceiba")
        if configuration_manager.validate_config_json():
            for entity in configuration_manager.put_the_order():
                entity_search_by_pid = IrokoRecordIterator(entity.get("pid"), stop_at=100)
                if entity_search_by_pid:
                    mapping = RDFMapper(create_graph, configuration_manager,
                                        entity_search_by_pid,
                                        entity.get("pid"))
                    graph = mapping._mapping_entity()
                    create_graph.graph = create_graph.graph + graph
                else:
                    print("Entity not found")
                    continue
            self.general_graph = create_graph.graph
            print(self.general_graph.serialize(format="ttl"))
        #     else:
        #         return False
        # except:
        #     return False
        return True

    # SELECT ?s ?p ?o WHERE { ?s ?p ?o FILTER (?o = "active") }
    def execute_sparql_query(self, sparql_query):
        """    Execute a SPARQL query on the graph.


        Args:
        sparql_query (str): The SPARQL query to execute.

        Returns:
        list: The query results as a list of rows.
        """
        try:
            qres = self.general_graph.query(sparql_query)
            results = []
            for row in qres:
                print("row", row)
                results.append(row)
            return results
        except Exception as e:
            print(f"An error occurred during the query: {str(e)}")
            return None

    def is_valid_sparql_query(self, query):
        """    Check if a SPARQL query is valid.


        Args:
        query (str): The SPARQL query to validate.

        Returns:
        bool: True if the query is valid, False otherwise.
        """
        try:
            parseQuery(query)
            return True
        except Exception:
            return False

    def get_entity_search_by_name(self, name: str):
        """    Get an entity search object based on the given name.


        Args:
        name (str): The name of the entity search.

        Returns:
        EntitySearch: An instance of the corresponding entity search class.
        """
        if name == "Organizations":
            return OrganizationSearch()
        elif name == "Sources":
            return SourceSearch()
        elif name == "Records":
            return RecordsSearch()

    def get_and_save_by_search_class(self, search_class):
        """    Get and save instances_iter based on the given search class.


        Args:
        search_class (type): The search class to retrieve instances_iter from.

        Returns:
        list: A list of instances_iter retrieved from the search class.
        """
        total_item = search_class
        offset = 0
        instances = []
        for item in total_item.scan():
            instances.append(item.to_dict())
            offset += 1
            if offset == 10:
                break
        with open('instances_iter.json', 'w') as file:
            json.dump(instances, file)
            print(f"Saved {offset} instances_iter of {search_class}")
        print("Process completed")
        return instances
