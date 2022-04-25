from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from envs.models import Envs
from envs.serializer import EnvsModelSerializer, EnvsNameModelSerializer
from rest_framework.response import Response
from envs.utils import process_env_data


class EnvsViewSet(ModelViewSet):
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer

    def list(self, request, *args, **kwargs):
        envs = super().list(request, *args, **kwargs)
        process_data = process_env_data(envs.data)
        return Response(process_data)

    @action(methods=['get'], detail=True)
    def EnvNames(self, request):
        instance = self.queryset()
        serializer_envs_name = EnvsNameModelSerializer(instance=instance, many=True)
        return Response(serializer_envs_name.data)