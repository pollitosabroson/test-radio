# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    """
    Abstract model that defines the 'public_id' field which is auto populated
    by a ramdom combination of 12 items iside the digits, lowercase and
    upercase letters.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name')
    )

    class Meta:
        abstract = True