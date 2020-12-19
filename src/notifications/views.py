# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
import base64
from datetime import datetime, timezone
import os

from django import forms, shortcuts, urls
from django.conf import settings
from django.contrib import messages
from django.core import exceptions, mail
from django.http import HttpResponseServerError
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _, ugettext_lazy
from django.views.decorators.http import require_http_methods, require_safe

from account import models as account_models
from account.decorators import auth_required

from . import models


class NotificationForm(forms.Form):
    email = forms.EmailField(label=ugettext_lazy('Email'))

class DeletionForm(forms.Form):
    pass


def _make_double_opt_in_secret():
    """
    Returns a base64-encoded double opt-in secret of 16 chars which contains
    96 bits of randomness (16 * 6b).
    """
    string_length = 16
    byte_length = string_length // 4 * 3
    return base64.b64encode(
        os.urandom(byte_length),
        altchars=b'/_'
    ).decode('utf-8')


def _make_double_opt_in_location(username, secret):
    return (
        urls.reverse('notifications:doi_confirm') +
        '?u={}&s={}'.format(username, secret)
    )


def _make_cancel_location(username, secret):
    return (
        urls.reverse('notifications:cancel') +
        '?u={}&s={}'.format(username, secret)
    )


def _send_email_from_template(recipients, subject, body_template, context):
    mail.send_mail(
        subject=subject,
        message=render_to_string(body_template, context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
    )


def _send_doi_mail(email, user, confirm_url, cancel_url):
    _send_email_from_template(
        recipients=(email,),
        subject=_('Please confirm your email address'),
        body_template='notifications/doi_mail.txt',
        context={
            'addresses': user.addresses,
            'confirm_url': confirm_url,
            'cancel_url': cancel_url,
        },
    )


def _send_doi_confirm_audit_mail(email, user, timestamp):
    _send_email_from_template(
        recipients=(settings.AUDIT_EMAIL,),
        subject='notifications double opt-in confirm',
        body_template='notifications/doi_confirm_audit_mail.txt',
        context={
            'email': email,
            'addresses': user.addresses,
            'timestamp': timestamp,
        },
    )


def _send_doi_cancel_audit_mail(email, user):
    _send_email_from_template(
        recipients=(settings.AUDIT_EMAIL,),
        subject='notifications double opt-in cancel',
        body_template='notifications/doi_cancel_audit_mail.txt',
        context={
            'email': email,
            'addresses': user.addresses,
            'timestamp': datetime.now(timezone.utc),
        },
    )


@require_http_methods(('GET', 'HEAD', 'POST'))
@auth_required
def index(request):
    try:
        u = account_models.User.objects.get(
            weblogin_username=request.user.username)
    except account_models.User.DoesNotExist:
        return HttpResponseServerError()

    try:
        n = models.Notification.objects.get(user=u)
    except models.Notification.DoesNotExist:
        n = None

    notification_form = NotificationForm(initial={
        'email': n.email if n else '',
    })
    deletion_form = DeletionForm()

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'delete':
            deletion_form = DeletionForm(request.POST)
            if deletion_form.is_valid():
                if n:
                    _send_doi_cancel_audit_mail(
                        email=n.email,
                        user=u,
                    )
                    n.delete()
                    messages.add_message(
                        request, messages.SUCCESS,
                        _('Email notifications are now disabled.'))

                return shortcuts.redirect('notifications:index')

        if action == 'save':
            notification_form = NotificationForm(request.POST)
            if notification_form.is_valid():
                email = notification_form.cleaned_data['email']

                if (not n) or (email != n.email):
                    secret = _make_double_opt_in_secret()
                    if not n:
                        n = models.Notification.objects.create(
                            user=u, email=email, double_opt_in_secret=secret,
                            confirmed=None)
                    else:
                        _send_doi_cancel_audit_mail(
                            email=n.email,
                            user=u,
                        )
                        n.email = email
                        n.double_opt_in_secret = secret
                        n.confirmed = None
                        n.save()

                    confirm_url = request.build_absolute_uri(
                        _make_double_opt_in_location(u.weblogin_username, secret)
                    )
                    cancel_url = request.build_absolute_uri(
                        _make_cancel_location(u.weblogin_username, secret)
                    )
                    _send_doi_mail(
                        email=email,
                        user=u,
                        confirm_url=confirm_url,
                        cancel_url=cancel_url,
                    )
                    messages.add_message(
                        request, messages.INFO,
                        _('A confirmation message has been sent to %(email)s.') %
                        {'email': email})

                return shortcuts.redirect('notifications:index')

    return shortcuts.render(request, 'notifications/index.html', context={
        'notification_form': notification_form,
        'deletion_form': deletion_form,
        'confirmed': n.confirmed if n else None,
    })


@require_safe
def doi_confirm(request):
    try:
        username = request.GET['u']
    except KeyError:
        raise exceptions.PermissionDenied

    try:
        secret = request.GET['s']
    except KeyError:
        raise exceptions.PermissionDenied

    try:
        u = account_models.User.objects.get(
            weblogin_username=username)
    except account_models.User.DoesNotExist:
        raise exceptions.PermissionDenied

    try:
        n = models.Notification.objects.get(
            user=u, double_opt_in_secret=secret)
    except models.Notification.DoesNotExist:
        raise exceptions.PermissionDenied

    if n.confirmed is None:
        timestamp = datetime.now(timezone.utc)
        n.confirmed = timestamp
        n.save()
        _send_doi_confirm_audit_mail(
            email=n.email,
            user=u,
            timestamp=timestamp,
        )

    return shortcuts.render(request, 'notifications/doi_confirm.html')


@require_safe
def cancel(request):
    try:
        username = request.GET['u']
    except KeyError:
        raise exceptions.PermissionDenied

    try:
        secret = request.GET['s']
    except KeyError:
        raise exceptions.PermissionDenied

    try:
        u = account_models.User.objects.get(
            weblogin_username=username)
    except account_models.User.DoesNotExist:
        raise exceptions.PermissionDenied

    try:
        n = models.Notification.objects.get(
            user=u, double_opt_in_secret=secret)
    except models.Notification.DoesNotExist:
        raise exceptions.PermissionDenied

    if n.confirmed is not None:
        _send_doi_cancel_audit_mail(
            email=n.email,
            user=u,
        )
    n.delete()

    return shortcuts.render(request, 'notifications/cancel.html')
