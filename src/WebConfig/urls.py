# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

import account.urls
import account.views
import notifications.urls


urlpatterns = [
    # Examples:
    # url(r'^$', 'WebConfig.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', account.views.login, name='login',
        kwargs={'redirect': 'account:index'}),
    url(r'^logout/$', account.views.logout, name='logout',
        kwargs={'redirect': 'account:loggedout'}),

    url(r'^status$', account.views.status, name='status'),

    url(r'^account/', include(account.urls, namespace='account')),
    url(r'^notifications/', include(notifications.urls, namespace='notifications')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
