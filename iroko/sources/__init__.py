# -*- coding: utf-8 -*-

#  Copyright (c) 2021. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


"""Iroko sources.
Los tipos de fuentes son:
    JOURNAL = "journal"
    STUDENT = "student"
    POPULARIZATION = "popularization"
    REPOSITORY = "repository"
    WEBSITE = "website"

En dependencia del tipo de fuente, existen diferentes marshmallows, apis, views, etc..

el api rest por defecto asume el source sin procesar el campo data.
las apis rest "herederas" lo que hacen es interpretar el campo data.
por ejemplo, las journals, interpretan el campo data, con los datos especificos de las revistas
academicas.



"""
