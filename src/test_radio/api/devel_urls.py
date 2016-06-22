# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.core.urlresolvers import clear_url_caches

from . import urls


# Patch the api url to include the debug_toolbar urls during development.
urlpatterns = urls.urlpatterns + [
    url(r'^__debug__/', include('debug_toolbar.toolbar', namespace='djdt')),
]


clear_url_caches()
