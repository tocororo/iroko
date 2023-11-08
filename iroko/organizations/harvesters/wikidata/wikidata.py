#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

from iroko.organizations.harvesters.wikidata.Controllers.dataCollect import collect, getDataInstance
from iroko.organizations.harvesters.wikidata.Controllers.instance import Instance


async def startCollect(org: str):
    await Instance.createTableInstance()
    await Instance.createTableSubclass()
    await collect(org)
    await getDataInstance('original')
    return org
