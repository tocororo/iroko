# Arreglos urgentes en los datos reales
repos = Repository.query.filter_by(status=HarvestedItemStatus.HARVESTED.value).all()
for re in repos:
    print(re.status)
    re.status = HarvestedItemStatus.RECORDED
    source = SourceRecord.get_record(re.source_uuid)
    source['repository_status'] = HarvestedItemStatus.RECORDED.value
    source.update()
    print(source['repository_status'])
db.session.commit()

from iroko.sources.api import SourceRecord

search = SourceRecord.get_search()
response = search[0:2000].execute()

for hit in response.hits:
     source = SourceRecord.get_record(hit['id'])
     if hit['source_type'] == 'JOURNAL':
         is_serial = True
         for identifier in hit['identifiers']:
             if identifier['idtype']=='oaiurl':
                 is_serial = False
                 print(source['name'], identifier['value'])
         if is_serial:
             source['source_type'] = 'SERIAL'
             source.update()

# Cosecha:

## OAI-PMH
 - La tarea mas importante por el momento es pensar en una interfaz para planificar todas las cosechas con celery.
 - supuestamente puede suceder que el harvester no recolecte todos los elementos de una revista, esto hay que chequearlo...

# Curaduria:

## Revistas

### Errores comunes

 - En los records pueden, en el campo descripcion y titulo, en varios idiomas, no separados por xml sino con una palabra como ABSTRACT.
    - **Posible solucion:** intentar identificar si en un campo hay mas de un idioma presente, o si alguna oracion no se corresponde con el idioma que se declara.

 - Puede suceder que los metadatos no se correspondan con el documento que describen: los autores, el titulo, etc... cuando se abre el documento no es el mismo. Es raro, pero paso en Mendive, Vol 2007 No 3, la editorial lo tiene.
    - **Posible solucion:** Habria que abordar el problema de extraer automaticamente los metadatos de los articulos y comparar entonces, cosa que en definitiva no puede demorarse mucho.


# Graph layer
Add an extra data layer using Neo4j



