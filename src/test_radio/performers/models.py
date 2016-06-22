# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from test_radio.core.db.models.basemodel import BaseModel

class Performer(BaseModel):

    class Meta:
        verbose_name = _('station')
        verbose_name_plural = _('stations')

    def __unicode__(self):
        return self.name