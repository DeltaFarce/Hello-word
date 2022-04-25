import re

from django.db.models import Count

from interfaces.models import Interfaces
from testcases.models import TestCases
from configures.models import Configures
from testsuits.models import TestSuits


def get_count_by_project(data):
    data_list = []
    for project in data:
        project['create_time'] = re.search('(.*)\.', project['create_time']).group(1)
        project['update_time'] = re.search('(.*)\.', project['update_time']).group(1)

        # 接口数量
        interfaces_cout = Interfaces.objects.filter(project_id=project['id'], is_delete=False).count()

        # 用例数量
        # case_count = 0
        # for interface in Interfaces.objects.filter(project_id=project['id'], is_delete=False):
        #     print(interface.id, "结果")
        #     testcases_count = TestCases.objects.filter(interface_id=interface.id, is_delete=False).count()
        #     case_count += testcases_count

        # 配置数量
        configure_count = 0
        for interface in Interfaces.objects.filter(project=project['id'], is_delete=False):
            configureCount = Configures.objects.filter(interfaces=interface.id, is_delete=False).count()
            configure_count += configureCount

        # print(configure_count)
        # print(Interfaces.objects.values('id').annotate(num_configure=Count('configures')).filter(project=project['id']
        # , is_delete=False))
        # configure_count2 = len(Interfaces.objects.annotate(num_configure=Count('configures')).filter(project=project
        # ['id'], is_delete=False))
        # print(configure_count2)

        # 套件数量
        # testsuit_count = TestSuits.objects.filter(project_id=project['id'], is_delete=False).count()

        # 将值添加到返回值中
        project['interfaces_cout'] = interfaces_cout
        # project['testsuits_cout'] = testsuit_count
        # project['testcases_cout'] = case_count
        project['configures_cout'] = configure_count
        data_list.append(project)
    return data_list
