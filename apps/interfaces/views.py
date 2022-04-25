from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from interfaces.models import Interfaces
from interfaces.serializer import InterfacesModelSerializer, InterfaceNameSerializer, InterfacesToConfiguresSerializer, \
    InterfacesToTestCasesSerializer
from interfaces.util import process_interfaces_data


class InterfacesViewSet(ModelViewSet):
    queryset = Interfaces.objects.filter(is_delete=False)
    serializer_class = InterfacesModelSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def InterfaceNames(self, request):
        instance = self.get_queryset()
        serializer = InterfaceNameSerializer(instance, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        interfaces_data = super().list(request, *args, **kwargs)
        interfaces_list = process_interfaces_data(interfaces_data.data)
        return Response(interfaces_list)

    @action(methods=['get'], detail=True)
    def configures(self, request, pk):
        instance = self.get_object()
        serializer = InterfacesToConfiguresSerializer(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def testcases(self, request, pk):
        serializer = InterfacesToTestCasesSerializer(instance=self.get_object())
        return Response(serializer.data)
