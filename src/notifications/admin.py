# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django.contrib import admin

from . import models


class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = (
        'user',
        'email',
        'double_opt_in_secret',
        'confirmed',
    )

admin.site.register(models.Notification, NotificationAdmin)
