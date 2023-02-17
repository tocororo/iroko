import yaml
import json 

def evaluate_category(category_name, responses):

    if category_name == 'Indización':
        return eval_indization(responses)

    if category_name == 'Acceso':
        return eval_Access(responses)

    if category_name == 'Interoperabilidad':
        return eval_Interoperability(responses)

    if category_name == 'Apertura':
        return eval_Opening(responses)

    if category_name == 'Internacionalización':
        return eval_Internationalization(responses)

    if category_name == 'Redes sociales':
        return eval_SocialNetworks(responses)

    if category_name == 'Impacto académico':
        return eval_AcademicImpact(responses)

    if category_name == 'Posición en rankings de revistas':
        return eval_PositionJournalRankings(responses)


def eval_indization(responses):
        
    if responses[0] == 'true' and responses[1] == 'true':
        return "ALTO", []
        
    if responses[0] == 'true' and responses[1] == 'false':
        return "MEDIO", [{'id': 'c_001_r_001', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'}]
 
    return "BAJO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales BAJO'}, { 'id' : 'c_003_r_001', 'value' : 'Implementar el protocolo OAI-PMH que permita la recopilación de metadatos por otros sistemas'}]

def eval_Access(responses):

    if responses[0] == 'true' and responses[3] == 'true':
        return "ALTO", []

    if responses[0] == 'true' and responses[3] == 'false':
        return "MEDIO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'}]

    return "BAJO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales BAJO'}, { 'id' : 'c_003_r_001', 'value' : 'Implementar el protocolo OAI-PMH que permita la recopilación de metadatos por otros sistemas'}]

def eval_Interoperability(responses):

    if responses[0] == 'true' and responses[1] == 'true':
        return "ALTO", []
        
    if responses[0] == 'true' and responses[1] == 'false':
        return "MEDIO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'}]

    return "BAJO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales BAJO'}, { 'id' : 'c_003_r_001', 'value' : 'Implementar el protocolo OAI-PMH que permita la recopilación de metadatos por otros sistemas'}]

def eval_Opening(responses):

    if responses[1] == 'true' and responses[2] == 'true':
        return "ALTO", []
        
    if responses[1] == 'true' and responses[2] == 'false':
        return "MEDIO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'}]

    return "BAJO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales BAJO'}, { 'id' : 'c_003_r_001', 'value' : 'Implementar el protocolo OAI-PMH que permita la recopilación de metadatos por otros sistemas'}]

def eval_Internationalization(responses):

    if responses[1] == 'true':
        return "ALTO", []
        
    return "MEDIO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'}]

def eval_SocialNetworks(responses):

    if responses[0] == 'true':
        return "ALTO", []
        
    return "MEDIO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'}]

def eval_AcademicImpact(responses):

    if responses[0] == 'true':
        return "ALTO", []
        
    return "MEDIO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'}]

def eval_PositionJournalRankings(responses):

    if responses[0] == 'NO':
        return "BAJO", [{'id': 'c_001_r_002', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales BAJO'}, { 'id' : 'c_003_r_001', 'value' : 'Implementar el protocolo OAI-PMH que permita la recopilación de metadatos por otros sistemas'}]

    return "ALTO", []
