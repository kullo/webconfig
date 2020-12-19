# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django.conf.urls import url

from . import views

app_name = 'account'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^loggedout/$', views.loggedout, name='loggedout'),
]
