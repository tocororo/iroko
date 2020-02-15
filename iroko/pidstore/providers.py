"""Iroko Providers."""
import uuid
from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.base import BaseProvider


class IrokoUUIDProvider(BaseProvider):
    """Document identifier provider."""

    pid_type = 'irouid'
    """Type of persistent identifier."""

    pid_provider = None
    """Provider name.
    The provider name is not recorded in the PID since the provider does not
    provide any additional features besides creation of record ids.
    """

    default_status = PIDStatus.REGISTERED
    """Record IDs are by default registered immediately.
    Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
    """

    @classmethod
    def create(cls, object_type=None, object_uuid=None, **kwargs):
        """Create a new record identifier from the depoist PID value."""
        if 'pid_value' not in kwargs:
            kwargs.setdefault('pid_value', str(uuid.uuid4()))
        kwargs.setdefault('status', cls.default_status)
        return super(IrokoUUIDProvider, cls).create(
            object_type=object_type, object_uuid=object_uuid, **kwargs)


class IrokoSourceOAIProvider(BaseProvider):
    """Provider in the form of {Source.uuid}-{Item.oaiIdentifier}
    When a record is harvested using OAI-PMH, is allways from a valid Source inside iroko, meaning that the Source must have an UUID.
    All items must have an oai identifier, since is harvested used OAI-PMH.
    So the persistent identifier use the form {Source.uuid}-{Item.oaiIdentifier}
    When migrating data across different installations of iroko, this need to be taken into consideration.
    """

    pid_type = 'srcoai'
    """Type of persistent identifier."""

    default_status = PIDStatus.REGISTERED
    """Record IDs are by default registered immediately.
    Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
    """

    @classmethod
    def create(cls, object_type=None, object_uuid=None, data=None,  **kwargs):
        """Create a new record identifier from the depoist PID value."""
        pid_value = cls.get_pid_from_data(data)
        if 'pid_value' not in kwargs:
            kwargs.setdefault('pid_value', pid_value)
        kwargs.setdefault('status', cls.default_status)
        return super(IrokoSourceOAIProvider, cls).create(
            object_type=object_type, object_uuid=object_uuid, **kwargs)

    @classmethod
    def get_pid_from_data(cls, data=None):
        assert data, "no data"
        assert 'source' in data, "no source in data"
        assert 'uuid' in data['source'], "no source uuid"

        oai_id=None
        for idf in data['identifiers']:
            if idf['idtype'] == 'oai':
                oai_id = idf['value']
        assert oai_id, "no oai in idenfitiers in data, or not value for it"

        return data['source']['uuid'] + '-' + oai_id
