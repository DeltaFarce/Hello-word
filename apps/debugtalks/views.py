from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from debugtalks.models import Debugtalks
from debugtalks.srializer import DebugtalksModelSerializer


class DebugtalksViewSet(ModelViewSet):
    queryset = Debugtalks.objects.all()
    serializer_class = DebugtalksModelSerializer

