# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
"""
WSGI config for WebConfig project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "WebConfig.settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
