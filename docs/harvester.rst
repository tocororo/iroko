..
    Copyright (C) 2019 UPR.

    iroko is free software; you can redistribute it and/or modify it under
    the terms of the MIT License; see LICENSE file for more details.


Harvester
========
Harvester module is the responsible for harvest research outputs from primary sources.

Models
------
.. automodule:: iroko.harvester.models

1- Repository: a source with a harvest_url.
2- HarvestedItem: a item harvested from a Repository.

OAI Harvester
---------
.. automodule:: iroko.harvester.oai.harvester

.. code-block::
        file_path = OaiFetcher.fetch_url(repo.harvest_endpoint)
        source_id = OaiFetcherProcessor.process_file(file_path)
        OaiArchivist.archive_source(source_id)

Views
-----

.. automodule:: iroko.harvester.rest
