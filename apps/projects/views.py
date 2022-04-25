from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from projects.serializer import ProjectsModelSerializer, ProjectsToInterfaces, InterfacesByProjectSerializer
from projects.models import Projects
from debugtalks.models import Debugtalks
from projects.utils import get_count_by_project


class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.filter(is_delete=False)
    serializer_class = ProjectsModelSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        Debugtalks.objects.create(project_id=serializer.data['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False)
    def names(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        # serializer = ProjectsToInterfaces(instance=Projects.objects.filter(is_delete=False), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def interfaces(self, request, pk):
        serializer = InterfacesByProjectSerializer(instance=self.get_object())
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response = get_count_by_project(response.data)
        return Response(response)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

