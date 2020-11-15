"""Source search APIs."""

from invenio_search import RecordsSearch


class IrokoRecordSearch(RecordsSearch):
    """RecordsSearch for sources."""

    class Meta:
        """Search only on sources index."""

        index = "records"
        doc_types = None

    def search_by_pid(self, *pids):
        """Retrieve sources with the given pid(s)."""
        return self.filter("terms", pid=pids)
