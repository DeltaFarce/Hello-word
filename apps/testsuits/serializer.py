from rest_framework.serializers import ModelSerializer
from testsuits.models import TestSuits


class TestSuitModelSerializer(ModelSerializer):
    class Meta:
        model = TestSuits
        fields = '__all__'
