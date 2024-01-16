#esta clase es l encargada  de establecer el orden en que se va a mapear ademas de validar el json de configuracion garantizando que tenga la estructura correcta 
class ConfigurationManager:
    def __init__(self, json_ontology_conf, namespace):
        self.json_ontology_conf = json_ontology_conf
        self.namespace = namespace
   
    def _get_json_ontology_conf():
      json_ontology_conf=json_ontology_conf
      return json_ontology_conf
    def _set_json_ontology_conf(new_json_ontology_conf):
      json_ontology_conf=new_json_ontology_conf
      return json_ontology_conf
      
    def validate_mapping_section(self, mapping_section):
        if not isinstance(mapping_section, dict):
            print("La sección 'mapping' debe ser un objeto JSON.")
            return False

        required_keys = ["_class", "required", "properties", "relationship", "valuesOf"]
        for key in required_keys:
            if key not in mapping_section:
                print(f"La clave '{key}' es requerida en la sección 'mapping'.")
                return False

        if not isinstance(mapping_section["required"], list):
            print("'required' debe ser una lista de nombres de propiedades requeridas.")
            return False

        if not isinstance(mapping_section["properties"], dict):
            print("'properties' debe ser un objeto JSON que mapea propiedades a URIs.")
            return False

        if not isinstance(mapping_section["relationship"], dict):
            print("'relationship' debe ser un objeto JSON que mapea relaciones a sus detalles.")
            return False

        if not isinstance(mapping_section["valuesOf"], dict):
            print("'valuesOf' debe ser un objeto JSON que mapea propiedades a sus valores permitidos.")
            return False

        return True

    def validate_entities(self, entities):
        for entity in entities:
            if "mapping" in entity:
                if not self.validate_mapping_section(entity["mapping"]):
                    return False
        return True

    def validate_config_json(self):
        if not isinstance(self.json_ontology_conf, dict):
            print("El archivo JSON debe contener un objeto JSON en la parte superior.")
            return False

        required_keys = ["name", "description", "created", "last_updated", "order_for_mapping", "entities"]
        for key in required_keys:
            if key not in self.json_ontology_conf:
                print(f"La clave '{key}' es requerida en el archivo JSON.")
                return False

        if not self.validate_entities(self.json_ontology_conf["entities"]):
            return False

        return True

    def put_the_order(self):
        if self.validate_config_json():
            order = self.json_ontology_conf.get("order_for_mapping", [])
            entities_map = {entity["name"]: entity for entity in self.json_ontology_conf.get("entities", [])}
            ordered_entities = [entities_map[name] for name in order if name in entities_map]
            return ordered_entities

        return None
