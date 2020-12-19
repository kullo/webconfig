# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django.db import connections, models
from django.db.models.functions import Coalesce, Length


class Plan(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(unique=True, max_length=50, editable=False)
    storage_quota = models.IntegerField(editable=False)

    def __str__(self):
        return '{} ({} GB)'.format(self.name, self.storage_quota / (1024*1024*1024))

    class KulloMeta:
        db_name = 'kulloserver'

    class Meta:
        ordering = ('storage_quota',)
        managed = False
        db_table = 'plans'


class User(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    registration_time = models.DateTimeField(editable=False)
    reset_code = models.CharField(max_length=50, blank=True, editable=False)
    weblogin_username = models.CharField(
        max_length=16, blank=True, editable=False)
    weblogin_secret = models.CharField(
        max_length=16, blank=True, editable=False)
    plan = models.ForeignKey('Plan', on_delete=models.PROTECT, editable=False)

    def __str__(self):
        return '#{}: {}'.format(self.id, self.weblogin_username)

    @property
    def addresses(self):
        return Address.objects \
        .filter(user=self) \
        .values_list('address', flat=True) \
        .order_by('address')

    @property
    def storage_used(self):
        try:
            return self.cached_storage_used
        except AttributeError:
            with connections[self.KulloMeta.db_name].cursor() as cursor:
                cursor.execute(
                    "SELECT coalesce(sum( "
                    "    coalesce(octet_length(content), 0) + "
                    "    coalesce(octet_length(keysafe), 0) + "
                    "    coalesce(octet_length(attachments), 0) "
                    "), 0) "
                    "FROM messages "
                    "WHERE user_id = (SELECT user_id FROM addresses WHERE address = %s) ",
                    [self.addresses[0]])
                row = cursor.fetchone()
                self.cached_storage_used = int(row[0])
                return self.cached_storage_used

    def storage_used_percent(self):
        return self.storage_used / self.plan.storage_quota * 100

    class KulloMeta:
        db_name = 'kulloserver'

    class Meta:
        ordering = ('id',)
        managed = False
        db_table = 'users'


class Address(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, editable=False)
    address = models.CharField(unique=True, max_length=50, editable=False)
    registration_code = models.CharField(
        max_length=50, blank=True, editable=False)

    def __str__(self):
        return self.address

    class KulloMeta:
        db_name = 'kulloserver'

    class Meta:
        verbose_name_plural = "addresses"
        ordering = ('address',)
        managed = False
        db_table = 'addresses'


class Message(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, editable=False)
    content = models.TextField(editable=False)
    keysafe = models.TextField(editable=False)
    attachments = models.BinaryField(editable=False)

    class KulloMeta:
        db_name = 'kulloserver'

    class Meta:
        managed = False
        db_table = 'messages'
