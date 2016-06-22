# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.importlib import import_module


def autodiscover():
    """
    Perform an autodiscover of an api.py file in the installed apps to
    generate the routes of the registered viewsets.
    """
    for app in settings.INSTALLED_APPS:
        try:
            import_module('.'.join((app, 'api')))

        except ImportError as e:
            pass
