# Copyright 2015–2020 Kullo GmbH
#
# This source code is licensed under the 3-clause BSD license. See LICENSE.txt
# in the root directory of this source tree for details.
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    import re
    request = context['request']
    if re.search(pattern, request.path):
        return 'active'
    return ''
