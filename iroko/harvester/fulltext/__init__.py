#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
from iroko.harvester.fulltext import ojs
from iroko.harvester.fulltext import dspace

OJS = "ojs"
DSPACE = "dspace"

get_files = {
    OJS: ojs.get_article_files,
    DSPACE: dspace.get_record_files
}
