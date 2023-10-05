# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, BNode
from rdflib.namespace import FOAF, XSD, OWL

"""Iroko Graph."""


class Create_Graph:

    def __init__(self, graph: Graph = None):
        """initialize the graph

        Args:
            graph (Graph, optional): _description_. Defaults to None.
        """
        if graph is None:
            self.graph = Graph()
        else:
            self.graph = graph
        # Defines a 'namespace' attribute as an empty dictionary
        self.namespace = {}

    def _add_triplet(self, sujeto, predicado, objeto):
        """adds a basic triple to the graph

        Args:
            sujeto (_type_): the subject of the triplete
            predicado (_type_): the predicate of the triplete
            objeto (_type_): the object of the triplete
        """
        try:
            # Check if subject is not an instance of URIRef or Literal
            if not isinstance(sujeto, (URIRef, Literal)):
                # Convert subject to URIRef
                sujeto = URIRef(sujeto)

            # Check if predicate is not an instance of URIRef or Literal
            if not isinstance(predicado, (URIRef, Literal)):
                # Convert predicate to URIRef
                predicado = URIRef(predicado)

            # Comprobar si objeto no es una instancia de URIRef o Literal
            if not isinstance(objeto, (URIRef, Literal)):
                # Intentar convertir objeto a URIRef si es una URI, o a Literal si es un literal
                if objeto.startswith('http://') or objeto.startswith('https://'):
                    objeto = URIRef(objeto)
                else:
                    objeto = Literal(objeto)

            # Agregar la tripleta al grafo
            self.graph.add((sujeto, predicado, objeto))

        except Exception as e:
            print(f"Error al agregar la tripleta: {str(e)}")

    def _serialize(self, format='ttl'):
        """
        Serializa el grafo RDF en el formato especificado.

        Args:
            format (str): Formato de serialización (ej. 'xml', 'turtle', 'n3', 'json-ld', etc.).

        Returns:
            str: Los datos RDF serializados en el formato especificado.
        """
        return self.graph.serialize(format=format, indent=True)

    def _add_namespaces(self, namespaces_dict):
        try:
            for prefix, namespace in namespaces_dict.items():
                self.graph.namespace_manager.bind(prefix, namespace)
            return self.graph  # Devuelve el grafo actualizado
        except Exception as e:
            print(f"Error al agregar namespaces: {str(e)}")
            return None  # Retorna None en caso de error

    def _get_namespaces(self):
        namespaces_dict = {}
        for prefix, uri in self.graph.namespaces():
            namespaces_dict[str(prefix)] = str(uri)
        return namespaces_dict

    # Verifica si existe una uri dada en el grafo

    def _uri_exists(self, uri):

        sujeto_uri = URIRef(uri)
        return (sujeto_uri, None, None) in self.graph
        # Busca una key dado su valor


class MappingtoRDF:
    def __init__(self, created_graph: Create_Graph, json_ontology_conf, json_instances, namespace: str):
        self.created_graph = created_graph
        self.json_ontology_conf = json_ontology_conf
        self.instances = json_instances
        self.namespace = namespace

    # Comprueba que la instancia sea un diccionario valido ,
    # que tenga una propiedad id y que la propiedad no este vacia
    # ,devuelve la uri del objeto

    def _validate_instance(self, instance):
        if not isinstance(instance, dict):
            print("Error: La instancia no es un diccionario válido.")
            return

        _id = instance.get("_id")

        if _id is None:
            print("Error: El atributo '_id' no se encuentra en la instancia JSON.")
            return
        else:
            # busca el namespace pasado por parametro en el dict de namespaces y lo guarda en una variable
            namespace = self.created_graph._get_namespaces()[self.namespace]
            for subj, pred, obj in self.created_graph.graph:
                if pred == _id:
                    print(pred)
                    print(_id)
                    # Encuentra una tripleta con el _id como predicado
                    # Modifica el sujeto con el namespace + _id
                    # Reemplaza con tu URI de sujeto modificado
                    new_subject = URIRef(f"{namespace}id/{_id}")
                    # Elimina la tripleta original
                    self.created_graph.graph.remove((subj, pred, obj))
                    # Agrega la nueva tripleta modificada
                    self.created_graph.graph.add((new_subject, pred, obj))

        return f"{namespace}id/{_id}"

  # Recibe el grafo como parametro y el namespace que va a tener las diferentes entidades en el gtrafo

    def _mapping_entity(self):

        if self.json_ontology_conf is None or self.instances is None:
            print("Error:El JSON es Nulo")
            return None

        # Inicializa uri_sceiba con un valor predeterminado
        uri_sceiba = None

        # Busca la uri de sceiba en el arreglo de namespaces del grafo
        uri_sceiba = self.created_graph._get_namespaces()["sceiba"]
        if uri_sceiba is None:
            print(f"Error: No se encontró la URI correspondiente ")
            return None

        for instance in self.instances:
            try:
                self._process_instance(instance)

            except Exception as instance_error:
                print(
                    f"Error al procesar la instancia JSON: {str(instance_error)}")
                print(f"Instancia JSON problemática: {instance}")
        rdf_data = self.created_graph._serialize(format='turtle')
        print(rdf_data)
   # recibe como parametro una llave un valor y la uri del sujeto
   # agrega la tripleta literal al grafo

    def _process_literal(self, key, value, subject):
        try:
            predicate = self.json_ontology_conf[key]
            object = value
            if value is not None:
                self.created_graph._add_triplet(
                    str(subject), str(predicate), str(object))
        except Exception as e:
            print(f"Error en process_literal: {str(e)}")
# devuelve verdadera si el diccionario es de identifiers

    def _is_identifiers(self, dictionary, list_of_identifiers):
        for identifier in list_of_identifiers:
            if identifier in dictionary:
                return True
        return False
# Procesa un diccionario con un identificador(campo identifier)

    def _process_identifiers_dict(self, subject, identifiers_dict):
        for key, value in identifiers_dict.items():
            object_value = ""
            predicate = ""
            if key == "idtype":
                predicate = self.json_ontology_conf[identifiers_dict[key]]
                object_value = identifiers_dict["idvalue"]
                self.created_graph._add_triplet(
                    str(subject), str(predicate), str(object_value))


# Procesa un diccionario mrecorre el dict y si el valor es no vacio pregunta si es

    def _process_dict(self, key, value_dict, subject):
        try:
            for key, value in value_dict.items():

                if self._is_identifiers(value_dict, ["idtype", "id"]):
                    self._process_identifiers_dict(subject, value_dict)
                else:
                    bnode = BNode()
                    self.created_graph._add_triplet(bnode, str(
                        self.json_ontology_conf[key]), str(value))
                    self.created_graph._add_triplet(
                        str(subject), str(self.json_ontology_conf[key]), bnode)

            return None
        except Exception as e:
            print(f"Error en _process_dict: {str(e)}")
            return None

         # procesa una  lista
    def _process_list(self, subject, key, value_list):
        # Pregunta para saber si es una lista de diccionarios o de literales
        try:
            if isinstance(value_list[0], dict):
                self._process_list_of_dict(subject, key, value_list)
            else:
                for literal in value_list:
                    self._process_literal(key, literal, subject)
        except Exception as e:
            print(f"Error en _process_list: {str(e)}")

    def _process_list_of_dict(self, subject, key, list_of_dict):
        for dict_item in list_of_dict:
            self._process_dict(key, dict_item, subject)

    def _process_relation(self, subject, key, id):
        try:
            bnode = BNode()
            self.created_graph._add_triplet(bnode, str(
                "https://w3id.org/cerif/model#Person.PersonIdentifier"), Literal(id))

            self.created_graph._add_triplet(str(subject), str(
                self.json_ontology_conf[key]), str(bnode))
        except Exception as e:
            print(f"Error en _process_relation: {str(e)}")

    def _process_relation_list(self, subject, key, list_of_relations):
        try:
            for relation in list_of_relations:
                self._process_relation(subject, key, relation)
        except Exception as e:
            print(f"Error en _process_relation_list: {str(e)}")

    def _process_instance(self, instance):

        # inicializa uri en una uri que devuelve el metodo _process_instance
        uri_of_the_subject = self._validate_instance(instance)
        # Pregunta si existe la uri en el grafo
        if not self.created_graph._uri_exists(uri_of_the_subject):
            try:
                # adiciona la tripleta al grafo
                self.created_graph._add_triplet(
                    (str(uri_of_the_subject)), RDF.type, (str(self.json_ontology_conf.get("_class"))))

            except Exception as triple_error:
                print(f"Error al agregar la tripleta: {str(triple_error)}")
        # Recorre las propiedades de la instancia
        for key, value in instance.items():
            try:
                # verifica que la key este en el json de configuracion y verifica que el valor sea no nulo
                if key in self.json_ontology_conf and instance[key] is not None:
                    predicate = key

                # verifica que no sea una instancia de list
                # procesa el literal
                    if not isinstance(value, (list, dict)):

                        self._process_literal(key, value, uri_of_the_subject)
                        # procesa un diccionario
                    if isinstance(value, (dict)):
                        self._process_dict(key, value, uri_of_the_subject)

                # Procesa si es una lista ya se lista de literales o de dict
                    if isinstance(value, list):
                        self._process_list(uri_of_the_subject, key, value)

                    if key == "afiliations":
                        if isinstance(value, list):
                            self._process_relation_list(
                                uri_of_the_subject, key, value)

                        else:
                            self._process_relation(
                                uri_of_the_subject, key, value)

                else:
                    print("la key no est en el json de config", key)

            except Exception as prop_error:
                print(
                    f"Error al procesar la propiedad '{key}': {str(prop_error)}")
