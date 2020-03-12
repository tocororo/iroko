
"""Source search APIs."""

from invenio_search import RecordsSearch

from iroko.taxonomy.api import Terms
from iroko.taxonomy.models import Term


class SourceSearch(RecordsSearch):
    """RecordsSearch for sources."""

    class Meta:
        """Search only on sources index."""

        index = "sources"
        doc_types = None

    def search_by_pid(self, *pids):
        """Retrieve sources with the given pid(s)."""
        return self.filter("terms", pid=pids)

    # @classmethod
    # def get_organization_buckets(cls, organizationUUID):
    #     term = Terms.get_term(organizationUUID)

    #     if term:


    #         query_body = {
    #             "query": {
    #                 "terms": {
    #                     "relations.uuid": terms
    #                 }
    #             }
    #         }
    #         return cls.from_dict(query_body).execute()

