def evaluate_journal(template, responses):

    evaluate_categories(template, responses)
    evaluate_sections(template, responses)
    final_evaluation(template, responses)

def evaluate_sections(template, responses):

    template['sections'][0]['titleEvaluationValue'] = eval_visibility(responses)
    template['sections'][1]['titleEvaluationValue'] = eval_impact(template, responses)

def eval_visibility(responses):

    var1 = ((not responses[0]) and
            (not responses[1]) and
            (int(responses[2]) + int(responses[3]) == 0))

    var2 = ((responses[4]) and
            (responses[5] == 'TODOS_NUM_PUBLICADOS_ULTIMOS_DOS_AÑOS') and
            (responses[6] == 'SI_DISPONIBLE_IND_SI_DESC_NUM') and
            (responses[8]))

    var3 = ((responses[9]) and
            (responses[10]) and
            (responses[11]) and
            (responses[13]) and
            (responses[15]))

    var4 = ((responses[17] == 'NO_PERMITE_AUTOARCHIVADO_VER') or
            (not responses[18]) or
            (not responses[19]) or
            (not responses[21]))

    var5 = ((responses[22] != 'EN_MAS_DE_UN_IDIOMA') or
            (responses[24] == 'MENOS_DEL_20') or
            (responses[25] == 'MENOS_DEL_20') or
            (responses[26] == 'MAS_DEL_50_TOTAL_PUBLICADO_PERIODO') or
            (responses[27] == 'MENOS_DEL_5_TOTAL_ART_ULT_DOS_AÑOS'))

    high = (not var1) and var2 and var3 and (not var4) and (not var5)

    if high:
        return 'ALTO'

    var1 = (responses[19] == responses[0])

    var2 = ((var1) and
            (responses[1]) and
            (int(responses[2]) + int(responses[3]) >= 1))

    var3 = ((not responses[4]) or
            (responses[6] == 'SI_DISPONIBLE_IND_NO_DESC_NUM') or
            (responses[6] == 'NO_DISPONIBLE_IND_NO_DESC_NUM') or
            (responses[5] == 'NO_DISPONIBLE_ULTIMO_NUM') or
            (responses[5] == 'NO_APLICA') or
            (not responses[7] and not responses[8]))

    var4 = ((not responses[9]) or
            (not responses[10]) or
            (not responses[11]) or
            (not responses[13]))

    var5 = ((responses[17] == 'NO_PERMITE_AUTOARCHIVADO_VER') or
            (not responses[18]) or
            (not responses[19]) or
            (not responses[21]))

    var6 = ((responses[22] != 'EN_MAS_DE_UN_IDIOMA') or
            (responses[24] == 'MENOS_DEL_20') or
            (responses[25] == 'MENOS_DEL_20') or
            (responses[26] == 'MAS_DEL_50_TOTAL_PUBLICADO_PERIODO') or
            (responses[27] == 'MENOS_DEL_5_TOTAL_ART_ULT_DOS_AÑOS'))

    low = (not var2) and var3 and var4 and var5 and var6

    if low:
        return 'BAJO'

    if (not high) and (not low):
        return 'MEDIO'

    return 'ERROR'

def eval_impact(template, responses):

    var1 = template['sections'][1]['categories'][0]['titleEvaluationValue']
    var2 = (var1 == 'ALTO') and (responses[34] != 'NO')

    if var2:
        return 'ALTO'

    if var1 == 'BAJO':
        return 'BAJO'

    if (not var2) and (var1 != 'BAJO'):
        return 'MEDIO'

    return 'ERROR'

def final_evaluation(template, responses):

    visibility = template['sections'][0]['titleEvaluationValue']
    impact = template['sections'][1]['titleEvaluationValue']

    if visibility == 'ALTO' and impact != 'BAJO':
        template['generalEvaluationValue'] = 'Nivel de calidad competitivo'

    if visibility == 'BAJO' and impact != 'ALTO':
        template['generalEvaluationValue'] = 'Nivel de calidad embrionario'

    template['generalEvaluationValue'] = 'Nivel de calidad en desarrollo'

def evaluate_categories(template, responses):

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

    if ((not responses[0]) and
        (responses[19])):

        recoms.append({'id': 'c_001_r_001', 'value': 'Postular revista a DOAJ'})

    if ((responses[31]) and
        (responses[32] == 'MAS_DEL_50_ART_ULT_3_AÑOS_REC_ALGUNA_CITA') and
        (responses[33] == 'MAYOR_IND_H5_REV_PER_ANT') and
        (not responses[1])):

        recoms.append({'id': 'c_001_r_002', 'value': 'Considerar la posibilidad de postular la revista a SCOPUS/Web de la Ciencia'})

    if (int(responses[2]) <= 1):
        recoms.append({'id': 'c_001_r_003', 'value': 'Postular revista a otras bases de datos de indización y resumen especializadas'})

    if (int(responses[3]) <= 1):
        recoms.append({'id': 'c_001_r_003', 'value': 'Postular revista a otras bases de datos de indización y resumen multidisciplinares'})

    var1 = (responses[19] == responses[0])

    var2 = ((var1) and
            (responses[1]) and
            (int(responses[2]) + int(responses[3]) >= 1))

    var3 = ((not responses[0]) and
            (not responses[1]) and
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

    if not responses[4]:
        recoms.append({'id': 'c_002_r_001', 'value': 'Crear el sitio web propio de la revista y solicitar el E-ISSN'})

    if ((responses[5] == 'NO_DISPONIBLE_ULTIMO_NUM') or
        (responses[5] == 'SOLAMENTE_DISPONIBLE_ULTIMO_NUM')):
        recoms.append({'id': 'c_002_r_002', 'value': 'Actualizar el sitio web propio de la revista con todos los números publicados en los últimos dos años'})

    if responses[5] == 'NO_APLICA':
        recoms.append({'id': 'c_002_r_003', 'value': 'Si crea un sitio web para la revista asegúrece de actualizarlo con todos los números publicados en los últimos dos años'})

    if responses[6] != 'SI_DISPONIBLE_IND_SI_DESC_NUM':
        recoms.append({'id': 'c_002_r_004', 'value': 'Evaluar cómo alinear las buenas prácticas de acceso abierto con las políticas editoriales'})

    var1 = (responses[7]) or (responses[8])

    if var1:
        recoms.append({'id': 'c_002_r_005', 'value': 'Promover el déposito de los artículos en repositorios internacionales, nacional, institucional, multidisciplinarios y tématicos'})

    var2 = ((responses[4]) and
            (responses[5] == 'TODOS_NUM_PUBLICADOS_ULTIMOS_DOS_AÑOS') and
            (responses[6] == 'SI_DISPONIBLE_IND_SI_DESC_NUM') and
            (responses[8]))

    var3 = ((not responses[4]) or
            (responses[6] == 'SI_DISPONIBLE_IND_NO_DESC_NUM') or
            (responses[6] == 'NO_DISPONIBLE_IND_NO_DESC_NUM') or
            (responses[5] == 'NO_DISPONIBLE_ULTIMO_NUM') or
            (responses[5] == 'NO_APLICA') or
            (not responses[7] and not responses[8]))

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

    if not responses[9]:
        recoms.append({'id': 'c_003_r_001', 'value': 'Emplear algún formato de metadatos (ej. Uso de OAI-DC , DC, Cerif, Mods, METS, etc.) para la descripción de sus publicaciones'})

    if not responses[10]:
        recoms.append({'id': 'c_003_r_002', 'value': 'Implementar el protocolo OAI-PMH que permita la recopilación de metadatos por otros sistemas'})

    if not responses[11]:
        recoms.append({'id': 'c_003_r_003', 'value': 'Completar en todos los artículos los metadatos definidos como obligatorios en el OpenAIRE Guidelines for Literature Repositories v3'})

    if not responses[12]:
        recoms.append({'id': 'c_003_r_004', 'value': 'Revisar que en todos los artículos estén los metadatos Field Language(Idioma), Field License Condition, Field Source, definidos como recomendables en el OpenAIRE Guidelines for Literature Repositories v3'})

    if not responses[13]:
        recoms.append({'id': 'c_003_r_005', 'value': 'Incluir entre sus metadatos Identificadores Persistentes de la publicación o relacionados a ella ( ej. ISSN-EISSN, DOI-Handle-URI-URN-Scopus ID-Wos ID-Scielo ID) en los campos Resource Identifier o Alternative Identifier según corresponda'})

    if not responses[14]:
        recoms.append({'id': 'c_003_r_006', 'value': 'Incluir como parte de su práctica editorial la solicitud del ORCID asociado al nombre de los autores y registrarlo como parte de sus metadatos'})

    if not responses[16]:
        recoms.append({'id': 'c_003_r_007', 'value': 'Explorar la posibilidad de incluir entre sus metadatos Identificador(es) Persistente(s) para organizaciones (ej.: GRID, ROR)'})

    var1 = ((responses[9]) and
            (responses[10]) and
            (responses[11]) and
            (responses[13]))

    var2 = var1 and (responses[15])
    var3 = var1 and (not responses[15])

    var4 = ((not responses[9]) or
            (not responses[10]) or
            (not responses[11]) or
            (not responses[13]))

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

    if not responses[18]:
        recoms.append({'id': 'c_004_r_002', 'value': 'En caso de no cobrar costo por procesamiento de artículos (APC), declararlo explicitamente en las políticas editoriales'})

    if not responses[19]:
        recoms.append({'id': 'c_004_r_003', 'value': 'Declarar explicitamente cuál es la política de acceso abierto de la revista'})

    if not responses[20]:
        recoms.append({'id': 'c_004_r_004', 'value': 'Promover el depósito de los datos de investigación en repositorios de acceso abierto como parte de su política editorial'})

    if not responses[21]:
        recoms.append({'id': 'c_004_r_005', 'value': 'Ofrecer sus contenidos bajo algun tipo de licencia Creative Common'})

    var1 = ((responses[17] != 'NO_PERMITE_AUTOARCHIVADO_VER') and
            (responses[18]) and
            (responses[19]) and
            (responses[21]) and
            (responses[6] == 'SI_DISPONIBLE_IND_SI_DESC_NUM'))

    var2 = ((responses[17] == 'NO_PERMITE_AUTOARCHIVADO_VER') or
            (not responses[18]) or
            (not responses[19]) or
            (not responses[21]))

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
            (responses[23]) and
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

    if not responses[28]:
        recoms.append({'id': 'c_006_r_001', 'value': 'Implementar funcionalidad de compartir contenidos en redes sociales'})

    if responses[29] == 'PERFIL_RED_SOC_SI_MENDELEY_RESEARCHGATE':
        recoms.append({'id': 'c_006_r_002', 'value': 'Crear y mantener activos perfiles tanto en redes sociales generales como en Mendeley y Researchgate para aumentar la difusión de sus publicaciones'})

    var1 = ((responses[31]) and
            (responses[29] == 'PERFIL_RED_SOC_SI_MENDELEY_RESEARCHGATE') and
            (responses[30] == 'TWITTER_FACEBOOK_INSTAGRAM_MENDELEY_RESEARCHGATE'))

    var2 = ((not responses[31]) or
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

    var1 = ((responses[31]) and
            (responses[32] == 'MAS_DEL_50_ART_ULT_3_AÑOS_REC_ALGUNA_CITA') and
            (responses[33] == 'MAYOR_IND_H5_REV_PER_ANT') and
            (responses[34] == 'Q1_Q2_JOURNAL_CITATION') and
            (responses[1]))

    var2 = ((responses[33] == 'NO_APLICA') or
            (responses[32] == 'MENOS_DEL_20_ART_ULT_3_AÑOS_REC_ALGUNA_CITA') or
            (not responses[31]))

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
