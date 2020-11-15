import jsonresolver

from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record


# the host corresponds to the config value for the key JSONSCHEMAS_HOST
@jsonresolver.route('/api/sources/<pid>', host='iroko.tocororo.cu')
def source_resolver(pid):
    """Resolve referenced user."""
    resolver = Resolver(pid_type='srcid', object_type="src",
                        getter=Record.get_record)
    _, record = resolver.resolve(pid)

    del record['$schema']
    return record
