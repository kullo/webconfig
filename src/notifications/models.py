# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, editable=False)
    email = models.EmailField(editable=False)
    double_opt_in_secret = models.CharField(max_length=16, editable=False)
    confirmed = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return '#{}: {}'.format(self.user.pk, self.email)

    class KulloMeta:
        db_name = 'kulloserver'

    class Meta:
        ordering = ('email',)
        managed = False
        db_table = 'notifications'
