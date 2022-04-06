#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

import logging
from iroko.config import WIKIDATA_LOG
logger = logging

logger.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                   datefmt='%I:%M:%S %p',
                   handlers=[
                       logging.FileHandler(WIKIDATA_LOG),
                       logging.StreamHandler()
                   ])

if __name__ == '__main__':
    logging.warning('mensaje a nivel warning')
    logging.info('mensaje a nivel info')
    logging.debug('mensaje a nivel debug')
    logging.error('Ocurrió un error en la base de datos')
    logging.debug('se realizó la conexión con exito')
