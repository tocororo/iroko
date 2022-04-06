#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

from iroko.organizations.harvesters.wikidata.logger_base import logger


class Subclass:
    def __init__(self, QID=None, label=None):
        self.__QID = QID
        self.__label = label

    def __str__(self):
        return (
            f'QID: {self.__QID}, '
            f'label: {self.__label}'
        )

    def getQID(self):
        return self.__QID

    def setQID(self, QID):
        self.__QID = QID

    def getItemLabel(self):
        return self.__label

    def setItemLabel(self, label):
        self.__label = label


if __name__ == '__main__':
    subclass = Subclass(QID='Q4564', label='Gomez')
    logger.debug(subclass)
