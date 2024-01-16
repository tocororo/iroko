# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, BNode
from rdflib.namespace import FOAF, XSD, OWL



class Create_Graph:
    def __init__(self, graph: Graph = None):
        """
        Initialize a Create_Graph.

        Args:
            graph (Graph, optional): The graph to work with. Defaults to None.
        """
        if graph is None:
        # If no graph is provided, create a new one
            self.graph = Graph()
        else:
            print(f"Error al agregar la tripleta: {str(e)}")
            self.graph = graph
        # Define an empty dictionary as the 'namespace' attribute
        self.namespace = {}

    def _add_triplet(self, sujeto, predicado, objeto):
        """    Add a triplet to the graph.


        Args:
            subject (any): The subject of the triplet.
            predicate (any): The predicate of the triplet.
            object (any): The object of the triplet.
        """
        try:
        # Check if subject is not an instance of URIRef or Literal
            if not isinstance(sujeto, (URIRef, Literal)):
            # Try to convert subject to URIRef
                sujeto = URIRef(sujeto)

        # Check if predicate is not an instance of URIRef
            if not isinstance(predicado, (URIRef, Literal)):
            # Try to convert predicate to URIRef
                predicado = URIRef(predicado)

        # Check if object is not an instance of URIRef or Literal
            if not isinstance(objeto, (URIRef, Literal)):
            # Try to convert object to URIRef if it's a URI, or to Literal if it's a literal
                if objeto.startswith('http://') or objeto.startswith('https://'):
                    objeto = URIRef(objeto)
                else:
                    objeto = Literal(objeto)

        # Add the triplet to the graph
            self.graph.add((sujeto, predicado, objeto))

        except Exception as e:
            print(f"Error while adding the triplet: {str(e)}")
        def serialize(self, format='ttl'):
            """    Serialize the RDF graph in the specified format.
    Args:
        format (str): Serialization format (e.g., 'xml', 'turtle', 'n3', 'json-ld', etc.).

            Returns:
        str: The RDF data serialized in the specified format.
            """
            return self.graph.serialize(format=format, indent=True)
        def add_namespaces(self, namespaces_dict):
            """    Add namespaces to the RDF graph.
        Args:
        namespaces_dict (dict): A dictionary where keys are namespace prefixes and values are namespaces.
        Returns:
        Graph: The updated graph after adding the namespaces.
            """
            try:
                for prefix, namespace in namespaces_dict.items():
                    self.graph.namespace_manager.bind(prefix, namespace)
                    return self.graph  # Returns the updated graph
            except Exception as e:
                    print(f"Error while adding namespaces: {str(e)}")
                    return None  # Returns None in case of an error
        #Verifica si existe una uri dada en el grafo
        def _uri_exists(self, uri):

            sujeto_uri = URIRef(uri)
            return (sujeto_uri, None, None) in self.graph
            #Busca una key dado su valor
