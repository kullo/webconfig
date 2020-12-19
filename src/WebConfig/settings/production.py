# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from WebConfig.settings import production_secrets as secrets
from WebConfig.settings.base import *


SECRET_KEY = secrets.SECRET_KEY
DATABASES['default']['PASSWORD'] = secrets.DB_PASSWORD
DATABASES['kulloserver']['PASSWORD'] = secrets.DB_PASSWORD

ALLOWED_HOSTS = ['accounts.kullo.net']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 15768000  # 6 months
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True

# admins are emailed on HTTP 500
ADMINS = [
    ['Daniel', 'daniel@kullo.net'],
]

STATIC_PRECOMPILER_DISABLE_AUTO_COMPILE = True
