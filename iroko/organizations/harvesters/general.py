#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

from iroko.organizations.api import OrganizationRecord
import traceback

def remove_nulls(d):
    return {k: v for k, v in d.items() if v is not None}


def _assing_if_exist(data, record, field):
    if field in record:
        data[field] = record[field]


def insert_in_organizations(data, inst):
    # try:
    OrganizationRecord.create_or_update(None, data, dbcommit=True, reindex=True)
    # except Exception as e:
    #     print(e)
    #     print("------------")
        #print(data)
        #print("------------")
        #print(inst)
        #print("------------")
        #print(traceback.format_exc())
