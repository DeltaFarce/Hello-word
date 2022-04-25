import datetime

from reports.models import Report
from rest_framework.serializers import ModelSerializer


class ReportsSerializer(ModelSerializer):
    class Meta:
        model = Report
        exclude = ('is_delete', 'update_time')
        extra_kwargs = {
            'html': {
                'write_only': True,
            },
            'create_time': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        name = validated_data['name']
        validated_data['name'] = name + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%s')
        report = Report.objects.create(**validated_data)
        report.save()
        return report
