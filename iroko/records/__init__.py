# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 UPR.
#
# iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.


"""sceiba project iroko software, invenio repository softwar"""

from __future__ import absolute_import, print_function

import enum

from .ext import iroko

__all__ = ('iroko', )

class ContributorRole(enum.Enum):

    Author = "Author"
    ContactPerson = "ContactPerson"
    DataCollector = "DataCollector"
    DataCurator = "DataCurator"
    DataManager = "DataManager"
    Distributor = "Distributor"
    Editor = "Editor"
    JournalManager = "JournalManager"
    Funder = "Funder"
    HostingInstitution = "HostingInstitution"
    Other = "Other"
    Producer = "Producer"
    ProjectLeader = "ProjectLeader"
    ProjectManager = "ProjectManager"
    ProjectMember = "ProjectMember"
    RegistrationAgency = "RegistrationAgency"
    RegistrationAuthority = "RegistrationAuthority"
    RelatedPerson = "RelatedPerson"
    ResearchGroup = "ResearchGroup"
    RightsHolder = "RightsHolder"
    Researcher = "Researcher"
    Sponsor = "Sponsor"
    Supervisor = "Supervisor"
    WorkPackageLeader = "WorkPackageLeader"
