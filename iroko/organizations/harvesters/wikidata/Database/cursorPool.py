#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

from iroko.organizations.harvesters.wikidata.Database.connection import Connection
# from iroko.organizations.harvesters.wikidata.logger_base import logger


class CursorPool:
    def __init__(self):
        self.__conn = None
        self.__cursor = None

    # inicio de with
    def __enter__(self):
        print('Start method __enter__')
        self.__conn = Connection.getConnection()
        self.__cursor = self.__conn.cursor()
        return self.__cursor

    # fin del bloque with
    def __exit__(self, exception_type, exception_value, exception_traceback):
        print('Execute method __exit__()')
        # if exception_value is not None:
        if exception_value:
            self.__conn.rollback()
            print(f'Error exception: {exception_value}')
        else:
            self.__conn.commit()
            print('Transaction commit')
            # Cerramos el cursor
        self.__cursor.close()
        # Regresar la conexión al pool
        Connection.releaseConnection(self.__conn)


if __name__ == '__main__':
    # Obtenemos un cursor  a partir de la conexión del pool
    # with se ejecuta __enter__ y termina con __exit__
    with CursorPool() as cursor:
        cursor.execute('SELECT * FROM "subClass"')
        print('Listado de personas')
        print(cursor.fetchall())
