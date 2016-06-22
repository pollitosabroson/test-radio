# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from test_radio.core.db.models.basemodel import BaseModel
from test_radio.performers.models import Performer

class Song(BaseModel):

    performer = models.ForeignKey(
        Performer, related_name='station'
    )

    class Meta:
        verbose_name = _('station')
        verbose_name_plural = _('stations')

    def __unicode__(self):
        return self.name