"""RPGuru Local Settings File"""

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['rpguru.test', 'localhost', '127.0.0.1']

LOGFILE = os.path.join(FILE_DIR, 'Projects/.log', 'rpguru.log')
LOGGING['handlers']['production']['filename'] = LOGGING['handlers']['debug']['filename'] = LOGFILE

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = secrets['email_host_user']
EMAIL_HOST_PASSWORD = secrets['email_host_password']
EMAIL_PORT = '2525'

# Django Debug Toolbar
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INTERNAL_IPS = ('127.0.0.1',)
