import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from configures.models import Configures
from configures.serializer import ConfiguresSerializer
from interfaces.models import Interfaces
from utils.handle_data import handle_data1, handle_data2


class ConfiguresViewSet(ModelViewSet):
    """
    处理请求头数据
    处理全局配置数据variables
    """
    queryset = Configures.objects.filter(is_delete=False)
    serializer_class = ConfiguresSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        configures = self.get_object()
        try:
            data_dict = json.loads(configures.request)
        except:
            handle_data = configures.request.replace('\'', '\"')
            data_dict = json.loads(handle_data)
        # 头部信息
        header_data = handle_data1(data_dict['config']['request']['headers'])
        # 参数信息
        variables_data = handle_data2(data_dict['config']['variables'])
        # 接口id
        selected_interface_id = configures.interfaces_id
        # 项目id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id

        serializer_data = {
            "author": configures.author,
            "configures_name": configures.name,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
            "header": header_data,
            "globalVar": variables_data
        }
        return Response(serializer_data)

