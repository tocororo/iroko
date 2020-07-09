
Una instalacion diferente a:
https://invenio.readthedocs.io/en/latest/quickstart/quickstart.html


Cumpliendo los requisitos
https://invenio.readthedocs.io/en/latest/general/requirements.html

=================================
Instalacion usando Ansible y lxd
=================================

- Instalar Ansible
- Crear contenedores.
- Ejecutar el playbook de invenio dependencies



ACCOUNTS_SESSION_REDIS_URL = 'redis://' + IP_REDIS + ':6379/1'
BROKER_URL = 'amqp://iroko:iroko@' + IP_RABBIT + ':5672/'
CACHE_REDIS_URL = 'redis://' + IP_REDIS + ':6379/0'
CACHE_TYPE = 'redis'
CELERY_BROKER_URL = 'amqp://iroko:iroko@' + IP_RABBIT + ':5672/'
CELERY_RESULT_BACKEND = 'redis://' + IP_REDIS + ':6379/2'
# SEARCH_ELASTIC_HOSTS='["http://"]'
params = dict(
    #    http_auth=('user', 'uRTbYRZH268G'),
)
SEARCH_ELASTIC_HOSTS = [
    dict(host=IP_ELASTIC, **params)
]
SECRET_KEY = 'iroko_secret_key'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://iroko:iroko@' + IP_POSGRE + '/iroko'
WSGI_PROXIES = 2
RATELIMIT_STORAGE_URL = 'redis://' + IP_REDIS + ':6379/3'
