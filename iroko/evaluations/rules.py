import yaml
import json 

def evaluate_category(template, responses):

    eval, recoms = eval_indization(responses)
    template['sections'][0]['categories'][0]['titleEvaluationValue'] = eval
    template['sections'][0]['categories'][0]['questionsOrRecoms'] = recoms

    eval, recoms = eval_access(responses)
    template['sections'][0]['categories'][1]['titleEvaluationValue'] = eval
    template['sections'][0]['categories'][1]['questionsOrRecoms'] = recoms

    eval, recoms = eval_interoperability(responses)
    template['sections'][0]['categories'][2]['titleEvaluationValue'] = eval
    template['sections'][0]['categories'][2]['questionsOrRecoms'] = recoms

    eval, recoms = eval_opening(responses)
    template['sections'][0]['categories'][3]['titleEvaluationValue'] = eval
    template['sections'][0]['categories'][3]['questionsOrRecoms'] = recoms

    eval, recoms = eval_internationalization(responses)
    template['sections'][0]['categories'][4]['titleEvaluationValue'] = eval
    template['sections'][0]['categories'][4]['questionsOrRecoms'] = recoms

    eval, recoms = eval_socialNetworks(responses)
    template['sections'][0]['categories'][5]['titleEvaluationValue'] = eval
    template['sections'][0]['categories'][5]['questionsOrRecoms'] = recoms

    eval, recoms = eval_academicImpact(responses)
    template['sections'][1]['categories'][0]['titleEvaluationValue'] = eval
    template['sections'][1]['categories'][0]['questionsOrRecoms'] = recoms

    eval, recoms = eval_positionJournalRankings(responses)
    template['sections'][1]['categories'][1]['titleEvaluationValue'] = eval
    template['sections'][1]['categories'][1]['questionsOrRecoms'] = recoms


def eval_indization(responses):

    recoms = []
    
    if ((responses[0] == 'false') and 
        (responses[19] == 'true')):

        recoms.append({'id': 'c_001_r_001', 'value': 'Postular revista a DOAJ'})

    if ((responses[31] == 'true') and 
        (responses[32] == 'MAS_DEL_50_ART_ULT_3_AÑOS_REC_ALGUNA_CITA') and 
        (responses[33] == 'MAYOR_IND_H5_REV_PER_ANT') and 
        (responses[1] == 'false')):

        recoms.append({'id': 'c_001_r_002', 'value': 'Considerar la posibilidad de postular la revista a SCOPUS/Web de la Ciencia'})

    if (int(responses[2]) <= 1):
        recoms.append({'id': 'c_001_r_003', 'value': 'Postular revista a otras bases de datos de indización y resumen especializadas'})

    if (int(responses[3]) <= 1):
        recoms.append({'id': 'c_001_r_003', 'value': 'Postular revista a otras bases de datos de indización y resumen multidisciplinares'})

    var1 = (responses[19] == responses[0])

    var2 = ((var1) and 
            (responses[1] == 'true') and 
            (int(responses[2]) + int(responses[3]) >= 1))

    var3 = ((responses[0] == 'false') and 
            (responses[1] == 'false') and 
            (int(responses[2]) + int(responses[3]) == 0))

    var4 = (not var2) and (not var3)

    if var2:
        return "ALTO", recoms
    
    if var4:
        return "MEDIO", recoms

    if var3:
        return "BAJO", recoms

    return "ERROR", recoms
         

def eval_access(responses):

    recoms = []

    if responses[4] == 'false':
        recoms.append({'id': 'c_002_r_001', 'value': 'Crear el sitio web propio de la revista y solicitar el E-ISSN'})

    if ((responses[5] == 'NO_DISPONIBLE_ULTIMO_NUM') or 
        (responses[5] == 'SOLAMENTE_DISPONIBLE_ULTIMO_NUM')):
        recoms.append({'id': 'c_002_r_002', 'value': 'Actualizar el sitio web propio de la revista con todos los números publicados en los últimos dos años'})

    if responses[5] == 'NO_APLICA':
        recoms.append({'id': 'c_002_r_003', 'value': 'Si crea un sitio web para la revista asegúrece de actualizarlo con todos los números publicados en los últimos dos años'})

    if responses[6] != 'SI_DISPONIBLE_IND_SI_DESC_NUM':
        recoms.append({'id': 'c_002_r_004', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'})

    var1 = (responses[7] == 'true') or (responses[8] == 'true')

    if var1:
        recoms.append({'id': 'c_002_r_005', 'value': 'Promover el déposito de los artículos en repositorios internacionales, nacional, institucional, multidisciplinarios y tématicos'})

    var2 = ((responses[4] == 'true') and 
            (responses[5] == 'TODOS_NUM_PUBLICADOS_ULTIMOS_DOS_AÑOS') and 
            (responses[6] == 'SI_DISPONIBLE_IND_SI_DESC_NUM') and 
            (responses[8] == 'true'))

    var3 = ((responses[4] == 'false') or 
            (responses[6] == 'SI_DISPONIBLE_IND_NO_DESC_NUM') or 
            (responses[6] == 'NO_DISPONIBLE_IND_NO_DESC_NUM') or
            (responses[5] == 'NO_DISPONIBLE_ULTIMO_NUM') or
            (responses[5] == 'NO_APLICA') or
            (responses[7] == 'false' and responses[8] == 'false'))

    var4 = (not var2) and (not var3)

    if var2:
        return 'ALTO', recoms

    if var4:
        return 'MEDIO', recoms

    if var3:
        return 'BAJO', recoms

    return 'ERROR', recoms

def eval_interoperability(responses):

    recoms = []

    if responses[9] == 'false':
        recoms.append({'id': 'c_003_r_001', 'value': 'Emplear algún formato de metadatos (ej. Uso de OAI-DC , DC, Cerif, Mods, METS, etc.) para la descripción de sus publicaciones'})

    if responses[10] == 'false':
        recoms.append({'id': 'c_003_r_002', 'value': 'Implementar el protocolo OAI-PMH que permita la recopilación de metadatos por otros sistemas'})

    if responses[11] == 'false':
        recoms.append({'id': 'c_003_r_003', 'value': 'Completar en todos los artículos los metadatos definidos como obligatorios en el OpenAIRE Guidelines for Literature Repositories v3'})

    if responses[12] == 'false':
        recoms.append({'id': 'c_003_r_004', 'value': 'Revisar que en todos los artículos estén los metadatos Field Language(Idioma), Field License Condition, Field Source, definidos como recomendables en el OpenAIRE Guidelines for Literature Repositories v3'})

    if responses[13] == 'false':
        recoms.append({'id': 'c_003_r_005', 'value': 'Incluir entre sus metadatos Identificadores Persistentes de la publicación o relacionados a ella ( ej. ISSN-EISSN, DOI-Handle-URI-URN-Scopus ID-Wos ID-Scielo ID) en los campos Resource Identifier o Alternative Identifier según corresponda'})

    if responses[14] == 'false':
        recoms.append({'id': 'c_003_r_006', 'value': 'Incluir como parte de su práctica editorial la solicitud del ORCID asociado al nombre de los autores y registrarlo como parte de sus metadatos'})

    if responses[16] == 'false':
        recoms.append({'id': 'c_003_r_007', 'value': 'Explorar la posibilidad de incluir entre sus metadatos Identificador(es) Persistente(s) para organizaciones (ej.: GRID, ROR)'})

    var1 = ((responses[9] == 'true') and 
            (responses[10] == 'true') and
            (responses[11] == 'true') and
            (responses[13] == 'true'))

    var2 = var1 and (responses[15] == 'true')
    var3 = var1 and (responses[15] == 'false')

    var4 = ((responses[9] == 'false') or
            (responses[10] == 'false') or
            (responses[11] == 'false') or
            (responses[13] == 'false'))

    if var2:
        return 'ALTO', recoms

    if var3:
        return 'MEDIO', recoms

    if var4:
        return 'BAJO', recoms

    return 'ERROR', recoms

def eval_opening(responses):

    recoms = []

    if responses[17] == 'NO_PERMITE_AUTOARCHIVADO_VER':
        recoms.append({'id': 'c_004_r_001', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'})

    if responses[18] == 'false':
        recoms.append({'id': 'c_004_r_002', 'value': 'En caso de no cobrar costo por procesamiento de artículos (APC), declararlo explicitamente en las políticas editoriales'})

    if responses[19] == 'false':
        recoms.append({'id': 'c_004_r_003', 'value': 'Declarar explicitamente cuál es la política de acceso abierto de la revista'})

    if responses[20] == 'false':
        recoms.append({'id': 'c_004_r_004', 'value': 'Promover el depósito de los datos de investigación en repositorios de acceso abierto como parte de su política editorial'})

    if responses[21] == 'false':
        recoms.append({'id': 'c_004_r_005', 'value': 'Ofrecer sus contenidos bajo algun tipo de licencia Creative Common'})

    var1 = ((responses[17] != 'NO_PERMITE_AUTOARCHIVADO_VER') and
            (responses[18] == 'true') and
            (responses[19] == 'true') and
            (responses[21] == 'true') and
            (responses[6] == 'SI_DISPONIBLE_IND_SI_DESC_NUM'))

    var2 = ((responses[17] == 'NO_PERMITE_AUTOARCHIVADO_VER') or
            (responses[18] == 'false') or
            (responses[19] == 'false') or
            (responses[21] == 'false'))

    var3 = (not var1) and (not var2)

    if var1:
        return 'ALTO', recoms

    if var3:
        return 'MEDIO', recoms

    if var2:
        return 'BAJO', recoms

    return 'ERROR', recoms

def eval_internationalization(responses):

    recoms = []

    if ((responses[25] != 'MAS_DEL_70') or
        (responses[24] != 'MAS_DEL_50')):

        recoms.append({'id': 'c_005_r_001', 'value': 'Aumentar la representación de expertos y especialistas externos a la institución editora, considerando mayor presencia de afiliados a instituciones extranjeras'})

    if responses[26] != 'MENOS_DEL_20_TOTAL_PUBLICADO_PERIODO':
        recoms.append({'id': 'c_005_r_002', 'value': 'Desarrollar mecanismos rigurosos que garanticen la conducta ética, la integridad académica, la resolución de conflictos de intereses y la transparencia en el proceso editorial según las buenas prácticas internacionales de publicación (ej. COPE guidelines,"&" ICMJE Recommendations)'})

    if responses[27] == 'MAS_DEL_25_TOTAL_ART_ULT_DOS_AÑOS':
        recoms.append({'id': 'c_005_r_003', 'value': 'Evaluar posibilidades para potenciar la revista como una vía para fortalecer la colaboración interinstitucional a nivel nacional e internacional'})

    var1 = ((responses[22] == 'EN_MAS_DE_UN_IDIOMA') and
            (responses[23] == 'true') and
            (responses[24] == 'MAS_DEL_50') and
            (responses[25] == 'MAS_DEL_70') and
            (responses[26] == 'MENOS_DEL_20_TOTAL_PUBLICADO_PERIODO') and
            (responses[27] == 'MAS_DEL_25_TOTAL_ART_ULT_DOS_AÑOS'))

    var2 = ((responses[22] != 'EN_MAS_DE_UN_IDIOMA') or
            (responses[24] == 'MENOS_DEL_20') or
            (responses[25] == 'MENOS_DEL_20') or 
            (responses[26] == 'MAS_DEL_50_TOTAL_PUBLICADO_PERIODO') or
            (responses[27] == 'MENOS_DEL_5_TOTAL_ART_ULT_DOS_AÑOS'))

    var3 = (not var1) and (not var2)

    if var1:
        return 'ALTO', recoms

    if var3:
        return 'MEDIO', recoms

    if var2:
        return 'BAJO', recoms

    return 'ERROR', []

def eval_socialNetworks(responses):

    recoms = []

    if responses[28] == 'false':
        recoms.append({'id': 'c_006_r_001', 'value': 'Implementar funcionalidad de compartir contenidos en redes sociales'})
 
    if responses[29] == 'PERFIL_RED_SOC_SI_MENDELEY_RESEARCHGATE':
        recoms.append({'id': 'c_006_r_002', 'value': 'Crear y mantener activos perfiles tanto en redes sociales generales como en Mendeley y Researchgate para aumentar la difusión de sus publicaciones'})

    var1 = ((responses[31] == 'true') and
            (responses[29] == 'PERFIL_RED_SOC_SI_MENDELEY_RESEARCHGATE') and
            (responses[30] == 'TWITTER_FACEBOOK_INSTAGRAM_MENDELEY_RESEARCHGATE'))

    var2 = ((responses[31] == 'false') or
            (responses[29] == 'NO') or
            (responses[30] == 'NO')) 

    var3 = (not var1) and (not var2)

    if var1:
        return 'ALTO', recoms

    if var3:
        return 'MEDIO', recoms

    if var2:
        return 'BAJO', recoms

    return 'ERROR', []

def eval_academicImpact(responses):

    var1 = ((responses[31] == 'true') and
            (responses[32] == 'MAS_DEL_50_ART_ULT_3_AÑOS_REC_ALGUNA_CITA') and
            (responses[33] == 'MAYOR_IND_H5_REV_PER_ANT') and
            (responses[34] == 'Q1_Q2_JOURNAL_CITATION') and
            (responses[1] == 'true'))

    var2 = ((responses[33] == 'NO_APLICA') or
            (responses[32] == 'MENOS_DEL_20_ART_ULT_3_AÑOS_REC_ALGUNA_CITA') or
            (responses[31] == 'false'))

    var3 = (not var1) and (not var2)

    if var1:
        return 'ALTO', []

    if var3:
        return 'MEDIO', [{'id': 'c_007_r_001', 'value': 'a) Orientar a los profesores que forman parte del consejo/comité editorial para el direccionamiento estratégico de la calidad de la revista, b) ofrecer pautas a los autores que les permitan mejorar el rigor y originalidad de los trabajos que envian a la revista indicándolas explícitamnete en las instrucciones a los autores y la política editorial así como en Editoriales, Cartas al editor o otros tipos de artículos publicados en la misma revista, c) mejorar la calidad de las revisiones a través de la mejora de los formularios de revisión, la elección de los revisores más adecuados para cada manuscrito, compartir las buenas prácticas de revisión, desarrollar competencias en los revisores novatos que les permitan reconocer las contribuciones potenciales de los manuscritos y cómo facilitar el desarrollo de ese potencial para elevar la calidad de los manuscritos aceptados y publicados'}]

    if var2:
        return 'BAJO', [{'id': 'c_007_r_001', 'value': 'a) Orientar a los profesores que forman parte del consejo/comité editorial para el direccionamiento estratégico de la calidad de la revista, b) ofrecer pautas a los autores que les permitan mejorar el rigor y originalidad de los trabajos que envian a la revista indicándolas explícitamnete en las instrucciones a los autores y la política editorial así como en Editoriales, Cartas al editor o otros tipos de artículos publicados en la misma revista, c) mejorar la calidad de las revisiones a través de la mejora de los formularios de revisión, la elección de los revisores más adecuados para cada manuscrito, compartir las buenas prácticas de revisión, desarrollar competencias en los revisores novatos que les permitan reconocer las contribuciones potenciales de los manuscritos y cómo facilitar el desarrollo de ese potencial para elevar la calidad de los manuscritos aceptados y publicados'}]

    return 'ERROR', []

def eval_positionJournalRankings(responses):

    if responses[34] == 'Q1_Q2_JOURNAL_CITATION':
        return 'ALTO', []

    if (responses[34] != 'Q1_Q2_JOURNAL_CITATION') and (responses[34] != 'NO'):
        return 'MEDIO', []
    
    if responses[34] == 'NO':
        return 'BAJO', []
    return 'ERROR', []