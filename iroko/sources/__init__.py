# -*- coding: utf-8 -*-
#
# This file is part of Iroko.
# Copyright (C) 2017, 2018 CERN.
#
# Iroko is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Iroko is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Iroko; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

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
por ejemplo, las journals, interpretan el campo data, con los datos especificos de las revistas academicas.



"""
