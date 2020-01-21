..
    Copyright (C) 2019 UPR.

    iroko is free software; you can redistribute it and/or modify it under
    the terms of the MIT License; see LICENSE file for more details.


.. include:: ../README.rst
TODO mejorar la documentacion de las reglas
Sources's Rules
------------
    Editor
    • Puede agregar una nueva fuente fuente
    • Al agregar fuente el siste envia notificacion a los gestores de los terminos
    • Puede editar una fuente, que si no esta aprobada seria la current
    • Al editar enviar notificacion a los gestores 
    •
    
    Gestor
    • Puede hacer lo mismo que el editor
    • Al editar una fuente esta siempre sera la current y se envia notificacion al editor
    • Puede cambiar el status de una fuente y se envia notificaicon al editor
    • Puede poner una version como current
    


    Generales
    • El usuario que incluye una fuente se le da el rol Editor de ese Source
    • Al editar un source, simplemente se crea una nueva version que sera current si es que el source no esta aprobado
    • Las fuentes nunca se eliminan, cada vez que se cambian datos en una se guerda una version de la misma
