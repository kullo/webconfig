# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from functools import wraps

from django.core.exceptions import PermissionDenied


def auth_required(viewfunc):
    """
    Checks whether user is authenticated. Raises PermissionDenied otherwise.
    """

    @wraps(viewfunc)
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return viewfunc(request, *args, **kwargs)

    return decorator
