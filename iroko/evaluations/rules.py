import yaml
import json 

def evaluate_category(template, responses):

    eval, recoms = eval_indization(responses)
    template['sections'][0]['categories'][0]['titleEvaluationValue'] = eval
    template['sections'][0]['categories'][0]['questionsOrRecoms'] = recoms


def eval_indization(responses):

    recoms = []
    
    if (responses[0] == 'false') and (responses[19] == 'true'):
        recoms.append({'id': 'c_001_r_001', 'value': 'Postular revista a DOAJ'})

    if (responses[32] == 'true') and (responses[33] == 'MAS_DEL_50_ART_ULT_3_AÑOS_REC_ALGUNA_CITA') and (responses[34] == 'MAYOR_IND_H5_REV_PER_ANT') and (responses[1] == 'false'):
        recoms.append({'id': 'c_001_r_002', 'value': 'Considerar la posibilidad de postular la revista a SCOPUS/Web de la Ciencia'})

    if (int(responses[2]) <= 1):
        recoms.append({'id': 'c_001_r_003', 'value': 'Postular revista a otras bases de datos de indización y resumen especializadas'})

    if (int(responses[3]) <= 1):
        recoms.append({'id': 'c_001_r_003', 'value': 'Postular revista a otras bases de datos de indización y resumen multidisciplinares'})

    var1 = (responses[19] == responses[0])
    var2 = var1 and (responses[1] == 'true') and (int(responses[2]) + int(responses[3]) >= 1)
    var3 = (responses[0] == 'false') and (responses[1] == 'false') and (int(responses[2]) + int(responses[3]) == 0)
    var4 = (not var2) and (not var3)

    if var2:
        return "ALTO", recoms
    
    if var4:
        return "MEDIO", recoms

    if var3:
        return "BAJO", recoms

    return "ERROR", []
         

def eval_access(responses):

    recoms = []

    if recoms[4] == 'false':
        recoms.append({'id': 'c_002_r_001', 'value': 'Crear el sitio web propio de la revista y solicitar el E-ISSN'})

    if (recoms[5] == 'NO_DISPONIBLE_ULTIMO_NUM') or (recoms[5] == 'SOLAMENTE_DISPONIBLE_ULTIMO_NUM'):
        recoms.append({'id': 'c_002_r_002', 'value': 'Actualizar el sitio web propio de la revista con todos los números publicados en los últimos dos años'})

    if recoms[5] == 'NO_APLICA':
        recoms.append({'id': 'c_002_r_003', 'value': 'Si crea un sitio web para la revista asegúrece de actualizarlo con todos los números publicados en los últimos dos años'})'

    if recoms[6] != 'Se acceden y descargan libremente de manera individual':
        recoms.append({'id': 'c_002_r_004', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'})

    var1 = (responses[7] == 'true') or (responses[8] == 'true')

    if var1:
        recoms.append({'id': 'c_002_r_005', 'value': 'Promover el déposito de los artículos en repositorios internacionales, nacional, institucional, multidisciplinarios y tématicos'})

    var2 = (responses[4] == 'true') and (recoms[5] == 'TODOS_NUM_PUBLICADOS_ULTIMOS_DOS_AÑOS') and (recoms[6] == 'SI_DISPONIBLE_IND_SI_DESC_NUM') and (recoms[8] == 'true')
    var3 = (responses[4] == 'false') or 

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
