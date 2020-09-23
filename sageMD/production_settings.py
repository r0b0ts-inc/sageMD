"""
Production Settings for Heroku
key:DJANGO_SETTINGS_MODULE
value:sageMD.production_settings
"""

from .development_settings import *

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env.str('SECRET_KEY')

ALLOWED_HOSTS = ['.herokuapp.com']

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db('DATABASE_URL'),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(env.str('ACCESS_TOKEN_LIFETIME'))),
}

# Debug in production-dev-environment
INTERNAL_IPS = [
    'iwise-backend-dev.herokuapp.com',
]

SITE_ID = env.int('SITE_ID')