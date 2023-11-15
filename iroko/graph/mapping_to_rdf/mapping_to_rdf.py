# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, BNode
from rdflib.namespace import FOAF, XSD, OWL


from os import name
from iroko.graph.mapping_to_rdf.configuration_manager import ConfigurationManager

from iroko.graph.mapping_to_rdf.create_graph import Create_Graph


class MappingtoRDF:
    def __init__(self, created_graph: Create_Graph, configurationManager: ConfigurationManager, json_instances, entity_name: str):
        self.created_graph = created_graph
        self.configurationManager = configurationManager
        self.instances = json_instances
        self.namespace = configurationManager.namespace
        self.entity_name = entity_name

   # Comprueba que la instancia sea un diccionario válido,
        # que tenga una propiedad id y que la propiedad no esté vacía
        # y devuelve la URI del objeto
    # valida que todos los requeridos esten en el json de una instancia
    def validate_required(self, required_attributes, instance):
        """Validates that all required attributes are present in the instance

        Args:
            required_attributes (list): A list of attribute names that are required.
        instance (dict): A dictionary representing the instance to validate.

    Returns:
        bool: True if all required attributes are present, False otherwise.

        """
    # Iterate over the list of required attributes
        for required_attribute in required_attributes:
            # If any required attribute is missing from the instance JSON, return False
            if required_attribute not in instance:
                return False
    # All required attributes are present in the instance JSON, so return True
        return True

# Dado un string nombre de entidad busca en las configuraciones su especifica configuracion
    def search_entity_by_string_name(self, entity_name: str):
        """Searches for the specific configuration 
        of an entity based on its name.

        Args:
        entity_name (str): The name of the entity.

        Returns:
        dict: The configuration of the entity if found,
          otherwise an empty dictionary.
        """
        entity_configuration = []
        for entity in self.configurationManager.json_ontology_conf.get("entities"):
            if entity["name"] == self.entity_name:
                entity_configuration = entity
                break

        return entity_configuration

    # valida que la instancia tenga los atributos requeridos en la configuracion
    def _validate_instance(self, instance):
        """Validates that the instance has the 
        required attributes specified in the 
        configuration.

        Args:
            instance (dict): A dictionary representing the instance to validate.

        Returns:
        str: The URI of the instance if it already exists in 
        the graph, otherwise returns the new URI.
                    Returns None if the instance does
                      not have all the required attributes.

        """
        required_attribute = self.search_entity_by_string_name(
            self.entity_name).get("mapping").get("required")

        if self.validate_required(required_attribute, instance):
            # Save the instance ID in a variable
            _id = instance.get("id")
        # Get the namespace from the namespaces dictionary using the provided namespace key
            namespace = self.created_graph._get_namespaces()[self.namespace]
            new_subject = f"{namespace}id/{_id}"
        # Iterate over the graph to check if the subject (URI) of the instance already exists
            for subject in self.created_graph.graph:
                # If it finds a match, return that subject (URI)
                if subject == new_subject:

                    return subject
        # If no match is found, return the new subject (URI)
            return new_subject
            # Return None if the instance does not have all the required attributes

        return None

    def validate_instances_array(self):
        if self.instances is None:
            print("Error: El JSON es Nulo")
            return False
        return True

      # se encarga de validar el arreglo de instancias ,inicializa la uri con la que se va a mapear las entidades
      # Si todo esta correcto procede a procesar las instancias
    def _mapping_entity(self):
        try:
            if self.validate_instances_array():
                uri_sceiba = None
                uri_sceiba = self.created_graph._get_namespaces().get(self.namespace)
                if uri_sceiba is None:
                    raise Exception("Error: No se encontró la URI correspondiente")
                else:
                    if self._process_instances(self.search_entity_by_string_name(self.entity_name).get("mapping")) == "Success":
                        rdf_data = self.created_graph
                        return rdf_data.graph
            else:
                raise Exception("Error: Invalid instances array")
        except Exception as e:
            return str(e)

    # Falta ultimar detalles
    def _process_literal(self, subject, key, value, properties_config):
        """Processes a literal value for a given subject and key 
        based on the properties configuration.

        Args:
            subject (_type_): _description_
            key (_type_): _description_
            value (_type_): _description_
            properties_config (_type_): _description_
        """
        try:
            predicate = properties_config[key]
            if isinstance(predicate, str):
                self.created_graph._add_triplet(
                    str(subject), str(predicate), str(value))
            if isinstance(predicate, list):
                for item in predicate:
                    self.created_graph._add_triplet(
                        str(subject), str(item), str(value))

        except Exception as e:
            print(f"Error en process_literal: {str(e)}")

    # Devuelve verdadero si el diccionario es de identifiers
    def _is_identifiers(self, value_dict: dict):
        """Checks if the given value_dict is an identifiers dictionary

        Args:
            value_dict (dict): _description_

        Returns:
        bool: True if the value_dict is an identifiers dictionary, False otherwise.
        """
        if "idtype" in value_dict.keys():
            return True

        return False

    # Procesa un diccionario con un identificador (campo identifier)
    def _process_identifiers_dict(self, subject, identifiers_dict: dict, identifiers_config: dict):
        """Processes the identifiers dictionary for a 
        given subject based on the identifiers configuration.


        Args:
        subject (_type_): _description_
        identifiers_dict (dict): A dictionary representing the identifiers for the subject.
        identifiers_config (dict): A dictionary representing the configuration for the identifiers.

        """
        try:
            # Get the predicate value from the identifiers_config dictionary based on the "__predicate" key
            # If the key is not found, use an empty string as the default value
            predicate = identifiers_config.get(
                identifiers_config.get("__predicate"), "")
        # Get the object value from the identifiers_dict dictionary based on the "__object" key
        # If the key is not found, use an empty string as the default value
            object_value = identifiers_dict.get(
                identifiers_config.get("__object"), "")
        # Add a triple to the created graph using the subject, predicate, and object value

            self.created_graph._add_triplet(
                str(subject), str(predicate), str(object_value))
        except Exception as e:
            # Print an error message if an exception occurs during the processing

            print(f"Error en _process_identifiers_dict: {str(e)}")
    # Procesa un diccionario, recorre el dict y si el valor no es vacío, pregunta si es

    def _process_dict(self, subject, key, value_dict: dict, properties_config:dict):
        """The  `_process_literal`  method receives the subject, key, a dictionary of 
        values ( `value_dict` ), and a properties configuration ( `properties_config` ) as arguments.
          Within the method, it checks if the value in the dictionary is another dictionary.
            In that case, it loops through each key-value pair of the inner dictionary using 
            recursion by calling the  `_process_literal`  method again.
            If the value in the dictionary is not a dictionary, it checks if it is a list. If it is, it loops
 through each element of the list using recursion.

Finally, if the value in the dictionary is neither a dictionary nor a list, it is directly added 
to the corresponding list in the properties configuration ( `properties_config` ).

In summary, the  `_process_literal`  method is responsible for processing a dictionary of values,
 recursively iterating through all the keys and values and adding them to the properties configuration.

I hope this clarifies the explanation for you. If you have any further questions, feel free to ask.

        Args:
            subject (_type_): The subject of the dictionary
            key (_type_): The key of the current dictionary entry
            value_dict (dict): The dictionary value to process
            properties_config (dict): The configuration of properties
        """
        try:
            # Create an empty list to store BNodes
            bnode_list = []
            for object_key, value in value_dict.items():
                predicate= properties_config.get(key).get(object_key)
                if isinstance(value,dict):
                # If the value is another dictionary, recursively call _process_dict

                    self._process_dict(subject,object_key,value,properties_config)
                else:
                    bnode = BNode() # Create a new BNode

                    if isinstance( predicate,list):
                        # If the predicate is a list, iterate over each item and add triplets to the graph

                        for predicate_item in predicate:
                            self.created_graph._add_triplet(str(bnode), str(
                    predicate_item), str(value))
                            bnode_list.append(bnode)
                    else:
                    # If the predicate is not a list, add a single triplet to the graph

                        self.created_graph._add_triplet(str(bnode), str(
                    predicate), str(value))
                        bnode_list.append(bnode)# Add the BNode to the list


            
            if predicate:
                    # If the key exists in properties_config, add triplets connecting the subject to the BNodes

                for bnode in bnode_list:
                    self.created_graph._add_triplet((subject), (
                properties_config.get(key).get(key)), bnode)

            else:
                # If the key does not exist in properties_config, add triplets connecting the subject to the BNodes using RDF.object

                self.created_graph._add_triplet(str(subject), RDF.object, bnode)
                print(subject,RDF.object,bnode)
        except Exception as e:
            print(f"Error en _process_dict: {str(e)}")

    # Procesa una lista
    def _process_list(self, subject, key, value_list, properties_config):
        try:
            if ((value_list != [])):
                for value in value_list:
                    self._process_literal(
                        subject, key, value, properties_config)
        except Exception as e:
            print(f"Error en _process_list: {str(e)}")

    def _process_list_of_dict(self, subject, key, list_of_dict, properties_config):
        for dict_item in list_of_dict:
            self._process_dict(key, dict_item, subject, properties_config)

    ''' def _process_relation(self, subject, key, id):
        try:
            bnode = BNode()
            self.created_graph._add_triplet(bnode, URIRef("https://w3id.org/cerif/model#Person.PersonIdentifier"), Literal(id))
            self.created_graph._add_triplet(str(subject), str(self.configurationManager._get_json_ontology_conf()[key]), str(bnode))
        except Exception as e:
            print(f"Error en _process_relation: {str(e)}")

    def _process_relation_list(self, subject, key, list_of_relations):
        try:
            for relation in list_of_relations:
                self._process_relation(subject, key, relation)
        except Exception as e:
            print(f"Error en _process_relation_list: {str(e)}") '''

# este metodo procesa  la seccion de de properties de una instancia o sea los atributos que repreentan un literal o una lista de literales
    def process_properties_in_an_instance(self, properties_config: dict, instance: dict, uri_of_the_subject):
        try:
            for key in properties_config.keys():
                value = instance.get(key)
                if value:

                    if isinstance(value, str):
                        self._process_literal(
                            uri_of_the_subject, key, value, properties_config)
                        continue

                   # if not isinstance(value, (list, dict)):
                        # Procesa un literal
                        #  self._process_literal(key,value,uri_of_the_subject,properties_config)

                    if isinstance(value, list):
                        if isinstance(value[0], str):

                            self._process_list(
                                uri_of_the_subject, key, value, properties_config)
                            continue
                        if isinstance(value[0], dict):
                            if self._is_identifiers(value[0]):
                                for identifier in value:
                                    self._process_identifiers_dict(
                                        uri_of_the_subject, identifier, properties_config.get("identifiers"))
                                continue
                            continue

                    if isinstance(value, dict):

                        self._process_dict(
                            uri_of_the_subject, key, value, properties_config)
                        continue
                else:
                    continue

        except Exception as e:
            print(f"Error al procesar propiedades en una instancia: {str(e)}")

    def process_relationship_in_an_instance():
        return 0

    def process_properties_section(self, properties_section_config,entity_class:str):
        for instance in self.instances:
            uri_of_the_subject = self._validate_instance(instance)
            self.created_graph._add_triplet(str(uri_of_the_subject),RDF.type,str(entity_class))
            self.process_properties_in_an_instance(
                properties_section_config, instance, uri_of_the_subject)
        

    def _process_instances(self, instance_configuration:dict):
        try:
            entity_class=instance_configuration.get("_class")
            self.process_properties_section(instance_configuration['properties'],entity_class)
            return "Success"
        except Exception as e:
            error_message = f"Error processing instances: {str(e)}"
            return error_message
