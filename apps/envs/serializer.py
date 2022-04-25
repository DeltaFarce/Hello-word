from envs.models import Envs
from rest_framework.serializers import ModelSerializer


class EnvsModelSerializer(ModelSerializer):
    class Meta:
        model = Envs
        fields = '__all__'


class EnvsNameModelSerializer(ModelSerializer):
    class Meta:
        model = Envs
        fields = ('id', 'name')
