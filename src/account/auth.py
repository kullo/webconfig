# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django.contrib.auth import models as djauth_models

from .models import User


class KulloAuthBackend(object):

    def authenticate(self, request, username=None, password=None):
        try:
            kullo_user = User.objects.get(weblogin_username=username)
        except User.DoesNotExist:
            return None

        secret = kullo_user.weblogin_secret
        if (len(secret) == 0) or (secret != password):
            return None

        try:
            return djauth_models.User.objects.get(username=username)
        except djauth_models.User.DoesNotExist:
            return djauth_models.User.objects.create_user(username=username)

    def get_user(self, user_id):
        try:
            return djauth_models.User.objects.get(pk=user_id)
        except djauth_models.User.DoesNotExist:
            return None
