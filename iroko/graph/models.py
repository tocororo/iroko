from typing import List, Dict, Union

class Configuration:
    def __init__(self, name: str, description: str, created: str, last_updated: str, order_for_mapping: List[str], entities: List['Entity']):
        self.name = name
        self.description = description
        self.created = created
        self.last_updated = last_updated
        self.order_for_mapping = order_for_mapping
        self.entities = entities

class Entity:
    def __init__(self, name: str, description: str, mapping: 'Mapping'):
        self.name = name
        self.description = description
        self.mapping = mapping

class Mapping:
    def __init__(self, _class: str, required: List[str],
     properties: Dict[str, Union[str, List[str], 'NestedMappings']], 
     valuesOf: Dict[str, Dict[str, str]]):
        self._class = _class
        self.required = required
        self.properties = properties
        self.valuesOf = valuesOf



class NestedMappings:
    def __init__(self, nested_mappings: Dict[str, List[str]]):
        self.nested_mappings = nested_mappings

class Relationship:
    def __init__(self, type: str, relation: str, description: str = None, identifier: str = None):
        self.type = type
        self.relation = relation
        self.description = description
        self.identifier = identifier

class Rule:
    def __init__(self, key: str, value: List[str]):
        self.key = key
        self.value = value