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
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('email', models.EmailField(editable=False, max_length=254)),
                ('double_opt_in_secret', models.CharField(editable=False, max_length=16)),
                ('confirmed', models.DateTimeField(null=True, blank=True, editable=False)),
            ],
            options={
                'managed': False,
                'db_table': 'notifications',
                'ordering': ('email',),
            },
        ),
    ]
