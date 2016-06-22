# -*- coding: utf-8 -*-
# flake8: noqa
from rest_framework.mixins import DestroyModelMixin as DeleteMixin
from rest_framework.mixins import RetrieveModelMixin as RetrieveMixin
from rest_framework.mixins import UpdateModelMixin as UpdateMixin

from .creation import CreateMixin
from .pagination import ListMixin
