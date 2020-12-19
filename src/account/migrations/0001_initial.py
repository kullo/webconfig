# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('address', models.CharField(unique=True, max_length=50, editable=False)),
                ('registration_code', models.CharField(editable=False, max_length=50, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'addresses',
                'verbose_name_plural': 'addresses',
                'ordering': ('address',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('registration_time', models.DateTimeField(editable=False)),
                ('reset_code', models.CharField(editable=False, max_length=50, blank=True)),
                ('weblogin_username', models.CharField(editable=False, max_length=16, blank=True)),
                ('weblogin_secret', models.CharField(editable=False, max_length=16, blank=True)),
            ],
            options={
                'managed': False,
                'db_table': 'users',
                'ordering': ('id',),
            },
        ),
    ]
