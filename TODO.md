
# Cosecha: 

## OAI-PMH
 - La tarea mas importante por el momento es pensar en una interfaz para planificar todas las cosechas con celery. 

# Curaduria: 

## Revistas

### Errores comunes

 - En los records pueden, en el campo descripcion y titulo, en varios idiomas, no separados por xml sino con una palabra como ABSTRACT. 
    - **Posible solucion:** intentar identificar si en un campo hay mas de un idioma presente, o si alguna oracion no se corresponde con el idioma que se declara. 

 - Puede suceder que los metadatos no se correspondan con el documento que describen: los autores, el titulo, etc... cuando se abre el documento no es el mismo. Es raro, pero paso en Mendive, Vol 2007 No 3, la editorial lo tiene. 
    - **Posible solucion:** Habria que abordar el problema de extraer automaticamente los metadatos de los articulos y comparar entonces, cosa que en definitiva no puede demorarse mucho. 



