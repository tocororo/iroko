

IP_ELASTIC = '192.168.56.3'
IP_POSGRE = '192.168.56.4'
IP_RABBIT = '192.168.56.6'
IP_REDIS = '192.168.56.5'

# IP_ELASTIC = '10.2.4.62'
# IP_POSGRE = '10.2.4.29'
# IP_RABBIT = '10.2.4.59'
# IP_REDIS = '10.2.4.58'

APP_ALLOWED_HOSTS = ['iroko.tocororo.cu', 'localhost', '127.0.0.1','10.80.4.34','10.2.83.193','10.2.83.159','10.2.83.160','192.168.1.100']


IROKO_HOST = 'https://localhost:5000'



ORCID_APP_CREDENTIALS = dict(
        consumer_key="APP-XXX",
        consumer_secret="secret",
)

IROKO_TEMP_DIRECTORY = '/tmp'

IROKO_DATA_DIRECTORY = 'data'

INIT_TAXONOMY_JSON_PATH = 'data/taxonomy.json'
INIT_JOURNALS_JSON_PATH = 'data/journals.json'
INIT_STATIC_JSON_PATH = 'data/texts'
INIT_OAIURL_JSON_PATH = 'data/oaisources.json'

HARVESTER_DATA_DIRECTORY='data/sceiba-data'
HARVESTER_SECONDARY_DIRECTORY='data/2_harvest_data'

REST_ENABLE_CORS = True

CUOR_API_ENDPOINT = 'https://localhost:5001/api/organizations'

# HARVESTER_DATA_DIRECTORY='/mnt/sceiba/sceiba-data'




# CORS_ORIGINS = ['https://localhost:5000','https://localhost:4200', 'http://10.2.83.101:4200/', 'https://10.2.83.101:4200/']
# CORS_RESOURCES = r'/api/*'
# CORS_SEND_WILDCARD = True
# CORS_SUPPORTS_CREDENTIALS=True
# CORS_EXPOSE_HEADERS = [u'ETag', u'Link', u'X-RateLimit-Limit', u'X-RateLimit-Remaining', u'X-RateLimit-Reset', u'Content-Type']
