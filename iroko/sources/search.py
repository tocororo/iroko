
"""Source search APIs."""

from elasticsearch_dsl.query import Q
from invenio_search import RecordsSearch
from invenio_search.api import DefaultFilter


def approveds_filter():
    """Filter approved sources."""
    return Q('bool', filter=[
        Q('match', **{'source_status': 'APPROVED'})
    ])

class SourceSearch(RecordsSearch):
    """RecordsSearch for sources."""

    class Meta:
        """Search only on sources index."""

        index = "sources"
        doc_types = None
        default_filter=DefaultFilter(approveds_filter)




        # if ids is not None:
        #     return list(map(lambda x: x, search.get_records(ids=ids)))
        # else:
        #     return list(map(lambda x: x, search.scan()))
