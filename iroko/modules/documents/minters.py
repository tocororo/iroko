
"""Document minters."""

from flask import current_app
from invenio_oaiserver.minters import oaiid_minter

from .providers import DocumentPidProvider


def build_document_pid(data, source):
        """Build document pid from record."""
        assert 'original_identifier' in data
        

        pid_value = (
            data.get('original_identifier')
        )
        return source + '-' + pid_value


def document_pid_minter(record_uuid, data, source):
    
    pid_field = current_app.config['PIDSTORE_RECID_FIELD']
    assert pid_field not in data
    pid_value = build_document_pid(data, source)
    provider = DocumentPidProvider.create(
        object_type='rec', pid_value=pid_value, object_uuid=record_uuid)
    
    return provider.pid
