"""RPGuru Local Settings File"""

from .base import *

DEBUG = False

# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
sentry_sdk.init(
    dsn=secrets['sentry_dsn'],
    integrations=[DjangoIntegration()],
    send_default_pii=True
)
