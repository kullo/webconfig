# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django.contrib import admin

from . import models


class PlanAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'name',
        'storage_quota',
    )


class UserAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'addresses',
        'plan',
        'storage_used_percent',
        'registration_time',
        'reset_code',
        'weblogin_username',
        'weblogin_secret',
    )


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = (
        'user',
        'address',
        'registration_code',
    )


admin.site.register(models.Plan, PlanAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Address, AddressAdmin)
