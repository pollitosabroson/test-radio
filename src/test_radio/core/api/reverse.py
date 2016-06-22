# -*- coding: utf-8 -*-
from urllib import urlencode
from urlparse import urlsplit, urlunsplit

from rest_framework.reverse import (
    reverse as rest_reverse, reverse_lazy as rest_reverse_lazy)


def add_querystring(method):
    """
    Decorator that appends the given query string to the reverse and
    reverse_lazy methods.
    """
    def wrapper(*args, **kwargs):
        querystring = kwargs.pop('query', {})
        url = method(*args, **kwargs)

        if querystring:
            scheme, netloc, path, query, fragment = urlsplit(url)
            query = urlencode(querystring, doseq=True)

            return urlunsplit((scheme, netloc, path, query, fragment))

        return url

    return wrapper


reverse = add_querystring(rest_reverse)
reverse_lazy = add_querystring(rest_reverse_lazy)
