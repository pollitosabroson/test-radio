# -*- coding: utf-8 -*-
from rest_framework import viewsets

from .models import Play
from .serializers import PlaySerializer
from test_radio.core.api.mixins import CreateMixin
from test_radio.api.v1.routers import router

class PlayViewSet(CreateMixin, viewsets.ViewSet):


    def create(self, request, *args, **kwargs):
        serializer = PlaySerializer(data=request.DATA)
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


router.register(r'plays', PlayViewSet, base_name='play')
