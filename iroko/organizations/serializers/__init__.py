from invenio_records_rest.serializers import record_responsify, search_responsify
from invenio_records_rest.serializers.json import JSONSerializer

from iroko.organizations.marshmallow.organization_v1 import OrganizationSchemaV1

# Serializers
# ===========
#: JSON serializer definition.

organization_v1 = JSONSerializer(OrganizationSchemaV1, replace_refs=True)

# Records-REST serializers
# ========================
#: JSON record serializer for individual records.
organization_v1_response = record_responsify(organization_v1, 'application/json')
#: JSON record serializer for search results.
organization_v1_search = search_responsify(organization_v1, 'application/json')
