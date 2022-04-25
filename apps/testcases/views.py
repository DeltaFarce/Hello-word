import json
import os.path
from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Laat2 import settings
from envs.models import Envs
from interfaces.models import Interfaces
from testcases.serializer import TestCaseModelSerializer, TestcasesRunserializer
from configures.models import Configures
from testcases.models import TestCases
from utils.common import generate_testcase_files, run_testcase
from utils.handle_data import handle_data1, handle_data2, handle_data3, handle_data5


class TestCaseViewSet(ModelViewSet):
    queryset = TestCases.objects.all()
    serializer_class = TestCaseModelSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        global include_data_dict
        testcases = self.get_object()
        include_data = testcases.include

        try:
            include_data = json.loads(include_data)
        except:
            include_data = include_data.replace('\'', '\"')
            include_data_dict = json.loads(include_data)
        # 全局配置
        include_config_data = Configures.objects.get(id=include_data_dict['config']).name

        # 前置用例
        include_testcases_case = TestCases.objects.filter(id__in=include_data_dict['testcases'])
        include_testcases_case_list = []
        for testcase in include_testcases_case:
            include_testcases_case_list.append(testcase.name)

        # 用例请求信息
        try:
            testcase_request = json.loads(testcases.request)
        except:
            data = testcases.request.replace('\'', '\"')
            testcase_request = json.loads(data)
        testcase_request_data = testcase_request.get('test').get('request')
        print("testcase_request_data请求信息:", testcase_request_data)

        # 处理用例variables变量列表
        if "variables" in testcase_request.get('test'):
            testcases_variables = testcase_request.get('test').get('variables')
            testcases_variables_list = handle_data2(testcases_variables)
        else:
            testcases_variables = ''
            testcases_variables_list = handle_data2(testcases_variables)

        # 处理用例header列表
        testcase_headers_list = handle_data1(testcase_request_data.get('headers'))

        # 处理params请求
        testcase_params = testcase_request_data.get('params')
        testcase_params_list = handle_data1(testcase_params)

        # 处理json请求
        testcase_json = testcase_request_data.get('json')
        testcase_json_list = handle_data1(testcase_json)

        # 处理extract
        testcase_extract = testcase_request.get('test').get('extract')
        testcase_extract_list = handle_data2(testcase_extract)

        # 处理validate
        testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate_list = handle_data3(testcase_validate)

        # 处理form表单数据
        testcase_form = testcase_request.get('test').get('data')
        testcase_form_list = handle_data3(testcase_form)

        # 处理parameters数据（参数化数据）
        testcase_parameters = testcase_request.get('test').get('parameters')
        testcase_parameters_list = handle_data2(testcase_parameters)

        # 处理setup_hooks数据
        testcase_setup_hooks = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_list = handle_data5(testcase_setup_hooks)

        # 处理teardown_hooks数据
        testcase_teardown_hooks = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_list = handle_data5(testcase_teardown_hooks)

        result = {
            "author": testcases.author,
            "testcase_name": testcases.name,
            "configure_id": include_data_dict.get('config'),
            "interfaces_id": testcases.interface_id,
            "project_id": Interfaces.objects.get(id=testcases.interface_id).project_id,
            "testcase_id": include_data_dict.get('testcases'),

            "method": testcase_request_data.get('method'),
            "url": testcase_request_data.get('url'),
            "formVariable": testcase_form_list,
            "jsonVariable": testcase_json_list,
            "params": testcase_params_list,
            "header": testcase_headers_list,

            "extract": testcase_extract_list,
            "validate": testcase_validate_list,
            "globalVal": testcases_variables_list,
            "parameters": testcase_parameters_list,
            "setup_hooks": testcase_setup_hooks_list,
            "teardown_hooks": testcase_teardown_hooks_list
        }

        return Response(result)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializer = TestcasesRunserializer(instance=instance, data=data)
        serializer.is_valid(raise_exception=True)
        case_data = serializer.validated_data
        # 获取运行环境
        env = Envs.objects.get(id=case_data.get('env_id'), is_delete=False).name

        # 指定生成文件夹路径
        testcase_dir_path_suites = os.path.join(settings.BASE_DIR, 'suites')
        testcase_dir_path = os.path.join(testcase_dir_path_suites, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        os.mkdir(testcase_dir_path)

        # 生成yaml文件夹
        generate_testcase_files(env, testcase_dir_path, instance)

        # 运行用例
        run_testcase(instance, testcase_dir_path)