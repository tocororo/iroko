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


# class IrokoURLSourceProvider(BaseProvider):
#     """Provider in the form of {Source.url}-{Item.identifier}
#     When a record is harvested, Source been harvested need an identifier, we take url in this case because is more likely that is universal and all source types need an url..
#     Also the record has a an identifier, global (url, or doi) and an internal identifier.
#     """

#     default_status = PIDStatus.REGISTERED
#     """Record IDs are by default registered immediately.
#     Default: :attr:`invenio_pidstore.models.PIDStatus.REGISTERED`
#     """

#     @classmethod
#     def create(cls, object_type=None, object_uuid=None, **kwargs):
#         """Create a new record identifier from the depoist PID value."""
#         if 'pid_value' not in kwargs:

#             kwargs.setdefault('pid_value', str(uuid.uuid4()))
#         kwargs.setdefault('status', cls.default_status)
#         return super(IrokoUUIDProvider, cls).create(
#             object_type=object_type, object_uuid=object_uuid, **kwargs)
