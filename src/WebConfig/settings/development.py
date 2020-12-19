# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from WebConfig.settings.base import *

DEBUG = True

SECRET_KEY = 'cnz1i$692*1$6lz(ik+*vc%yb+47dstfr_^lckd-8(+fm&)1_s'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]
