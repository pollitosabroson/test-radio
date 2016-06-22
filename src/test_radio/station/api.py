# -*- coding: utf-8 -*-
from rest_framework import viewsets

from .models import Station
from .serializers import StationSerializer
from test_radio.core.api.mixins import CreateMixin
from test_radio.api.v1.routers import router

class StationViewSet(CreateMixin, viewsets.ViewSet):


    def create(self, request, *args, **kwargs):
        serializer = StationSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


router.register(r'station', StationViewSet, base_name='station')