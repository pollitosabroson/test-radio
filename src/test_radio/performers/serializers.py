# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Performer


class PerformerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performer
        fields = [
            'name',
        ]