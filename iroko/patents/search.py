
"""Source search APIs."""

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

from invenio_search import RecordsSearch


class PatentsSearch(RecordsSearch):
    """RecordsSearch for sources."""

    class Meta:
        """Search only on organizations index."""

        index = "patents"
        doc_types = None
