from rest_framework.viewsets import ModelViewSet
from testsuits.models import TestSuits
from testsuits.serializer import TestSuitModelSerializer


class TestSuitViewSet(ModelViewSet):
    queryset = TestSuits.objects.all()
    serializer_class = TestSuitModelSerializer
