import datetime
import os
import re

from django.utils.encoding import escape_uri_path
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from reports.models import Report
from reports.serializer import ReportsSerializer
from reports.utils import format_report_reponse, format_report, get_file_contents_byte
from Laat2.settings import REPORTS_DIR
from django.http import StreamingHttpResponse


class ReportsViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportsSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # print(response.data)
        report_data = format_report_reponse(response.data)
        return Response(report_data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        print(response.data)
        report = format_report(response.data)
        return Response(report)

    @action(methods=['get'], detail=True)
    def download(self, request, pk):
        report = self.get_object()
        html = report.html
        name = report.name
        report_name = re.search(r'(.*_)\d', name)
        if report_name:
            report_name = report_name.group(1) + datetime.datetime.now().strftime('%Y%m%d%H%M%s') + '.html'
            print(report_name, "report_name名称")
        else:
            report_name = name

        report_path = os.path.join(REPORTS_DIR, report_name)
        print(report_path, "report_path路径")
        with open(report_path, 'w+', encoding='utf-8') as f:
            f.write(html)
        response = StreamingHttpResponse(get_file_contents_byte(report_path))
        # 防止中文乱码
        report_path_final = escape_uri_path(report_name)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = "attachment:filename*=UTF-8''{}".format(report_path_final)
        return response
