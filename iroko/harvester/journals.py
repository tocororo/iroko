

from iroko.modules.sources.models import Sources

def harvest_journal(uuid):
    src = Sources.query.filter_by(uuid=uuid).first()

    enpoint = src.havest_endpoint
    