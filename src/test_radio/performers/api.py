# -*- coding: utf-8 -*-
from rest_framework import viewsets

from .models import Performer
from .serializers import PerformerSerializer
from test_radio.core.api.mixins import CreateMixin
from test_radio.api.v1.routers import router

class PerformerViewSet(CreateMixin, viewsets.ViewSet):


    def create(self, request, *args, **kwargs):
        serializer = PerformerSerializer(data=request.DATA)
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


router.register(r'performers', PerformerViewSet, base_name='performer')
