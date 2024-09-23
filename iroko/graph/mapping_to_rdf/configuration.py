import json

class EntityMapping:
    def __init__(self, entity: dict):
        self.pid = self.config['pid']
        self.name = self.config['name']
        self.description = self.config['description']
        self._class = self.config['_class']
        self.required = self.config['required']
        self.properties = self.config['properties']
        self.valuesof = self.config['valuesOf']

class Mapping:

    def __init__(self, config: dict):
        self.config = config
        self.name = self.config['name']
        self.description = self.config['description']
        self.created = self.config['created']
        self.last_updated = self.config['last_updated']
        self._order = self.config['_order']

        entities = [EntityMapping(entity) for entity in self.config['entities']]
        entities_map = {entity.pid: entity for entity in entities}
        ordered_entities = [entities_map[pid] for pid in self.mapping_order if pid in entities_map]
        self.mappings = ordered_entities


