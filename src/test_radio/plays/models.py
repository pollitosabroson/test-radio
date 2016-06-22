from django.db import models

from test_radio.songs.models import Song
from test_radio.station.models import Station

# Create your models here.

class Play(models.Model):

    song = models.ForeignKey(
        Song,
        related_name='song'
    )

    station = models.ForeignKey(
        Station,
        related_name='station'
    )

    start_play = models.DateTimeField()

    end_play = models.DateTimeField()

    def __unicode__(self):
        return self.song