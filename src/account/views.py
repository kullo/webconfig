# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django import shortcuts
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.db import connections
from django.http.response import HttpResponseServerError
from django.views.decorators.http import require_safe

from . import models
from .decorators import auth_required


@require_safe
def status(request):
    try:
        cursor = connections['default'].cursor()
        cursor.close()
    except:
        return HttpResponseServerError()

    return shortcuts.render(
        request, 'account/status.html'
    )


@require_safe
def login(request, redirect):
    if request.user.is_authenticated:
        auth.logout(request)

    try:
        username = request.GET['u']
    except KeyError:
        raise PermissionDenied

    try:
        secret = request.GET['s']
    except KeyError:
        raise PermissionDenied

    user = auth.authenticate(request, username=username, password=secret)
    if user is None:
        raise PermissionDenied
    if not user.is_active:
        raise PermissionDenied

    auth.login(request, user)
    return shortcuts.redirect(redirect)


@require_safe
def logout(request, redirect):
    if request.user.is_authenticated:
        auth.logout(request)
    return shortcuts.redirect(redirect)

@require_safe
def loggedout(request):
    return shortcuts.render(
        request, 'account/loggedout.html'
    )

@require_safe
@auth_required
def index(request):
    try:
        user = models.User.objects.get(weblogin_username=request.user.username)
    except models.User.DoesNotExist:
        return HttpResponseServerError()

    return shortcuts.render(
        request, 'account/index.html',
        context={
            'kullo_user': user,
        }
    )
