# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Play


class PlaySerializer(serializers.ModelSerializer):

    song = serializers.CharField(
        source='song.name'
    )

    station = serializers.CharField(
        source='station.name'
    )

    class Meta:
        model = Play
        fields = [
            'song', 'station',
            'start_play', 'end_play',
        ]