#!/usr/bin/env bash
#
# Copyright (c) 2022. Universidad de Pinar del Rio
# This file is part of SCEIBA (sceiba.cu).
# SCEIBA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE ROLE iroko WITH LOGIN PASSWORD 'iroko';
    ALTER ROLE iroko CREATEDB;
    \du;
EOSQL
