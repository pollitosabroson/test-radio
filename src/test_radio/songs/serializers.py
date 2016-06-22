# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Song


class SongSerializer(serializers.ModelSerializer):

    performers = serializers.CharField(
        source='performer.name'
    )

    class Meta:
        model = Song
        fields = [
            'name',
            'performers',
        ]