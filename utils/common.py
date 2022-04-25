import json
import os.path
from datetime import datetime

import yaml
from rest_framework import status
from rest_framework.response import Response

from configures.models import Configures
from debugtalks.models import Debugtalks
from reports.models import Report
from testcases.models import TestCases
from httprunner import HttpRunner


def generate_testcase_files(instance, env, testcase_dir_path):
    testcase_list = []

    # 前置配置和前置用例

    include = json.loads(instance.include)

    # 本身用例请求信息
    request = json.loads(instance.request)

    # 接口名称
    interface_name = instance.interface.name

    # 项目名称
    project_name = instance.interface.project.name
    # 生成项目文件夹，并且将对应项目的debugtalk中的定义函数复制过来
    project_dir_path = os.path.join(testcase_dir_path, project_name)
    # 写入debugtalk.py文件
    if not os.path.exists(project_dir_path):
        os.mkdir(project_dir_path)
        debugtalk_obj = Debugtalks.objects.filter(is_delete=False, project__name=project_name).first()
        if debugtalk_obj:
            debugtalks = debugtalk_obj.debugtalk
        else:
            debugtalks = ''
        with open(os.path.join(project_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as file:
            file.write(debugtalks)

    # 生成接口文件夹
    interface_dir_path = os.path.join(project_dir_path, interface_name)
    if not os.path.exists(interface_dir_path):
        os.mkdir(interface_dir_path)

    # 前置配置
    config_id = include.get('config')
    if config_id is not None:
        Config_obj = Configures.objects.filter(id=config_id, is_delete=False).first()
        Config_request = json.loads(Config_obj.request)
        Config_request.get('config').get('request').setdefault('base_url', env.base_url)
        Config_request['config']['name'] = instance.name
        print("Config_request数据2", Config_request)
        testcase_list.append(Config_request)

    # 获取前置用例
    testcases_id = include.get('testcases')
    if testcases_id is not None:
        for case_id in testcases_id:
            testcases_obj = TestCases.objects.get(id=case_id)
            case = json.loads(testcases_obj.request)
            testcase_list.append(case)

    testcase_list.append(json.loads(instance.request))
    print("testcase_list数据", testcase_list)
    # 写入yaml文件
    with open(os.path.join(interface_dir_path, instance.name + '.yaml'), 'w', encoding='utf-8') as file:
        yaml.dump(testcase_list, file, allow_unicode=True)


# 运行用例
def run_testcase(instance, testcase_dir_path):
    runner = HttpRunner()
    runner.run(testcase_dir_path)  # 运行用例

    # 生成报告
    try:
        report_name = instance.name
    except Exception as e:
        report_name = "被遗弃的报告"
    report_id = create_report(runner, report_name=report_name)
    return Response(report_id, status=status.HTTP_202_ACCEPTED)


# 获取测试报告
def create_report(runner, report_name):
    # 数据格式处理
    time_stamp = runner.summary['time']['start_at']
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    for item in runner.summary['details']:
        for record in item['records']:
            record['meta_data']['response']['content'] = record['meta_data']['response']['content'] .decode('utf-8')
            record['meta_data']['response']['cookie'] = record['meta_data']['response']['cookies']
            if isinstance(record['meta_data']['request']['body'], bytes):
                record['meta_data']['request']['body'] = record['meta_data']['request']['body'].decode('utf-8')

    # summary转换成json格式
    summary = json.dumps(runner.summary, ensure_ascii=False)
    report_name = report_name if report_name else runner.summary['time']['start_at']
    report_name = report_name + datetime.strftime(datetime.now(), '%Y%m%d%%HM%S')
    report_name = runner.gen_html_report(html_report_name=report_name)
    with open(report_name, 'r') as f:
        report = f.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': report,
        'summary': summary
    }
    report_obj = Report.objects.create(**test_report)
    return report_obj.id
