from rest_framework import serializers

from configures.serializer import InterfacesAnotherSerializer
from envs.models import Envs
from testcases.models import TestCases
from rest_framework.serializers import ModelSerializer


class TestCaseModelSerializer(ModelSerializer):
    interface = InterfacesAnotherSerializer(help_text='所属项目和接口信息')

    class Meta:
        model = TestCases
        fields = ('id', 'name',  'include', 'author', 'request', 'interface')
        # extra_kwargs = {
        #     'include': {
        #         'write_only': True
        #     },
        #     'request': {
        #         'write_only': True
        #     }
        # }

    def create(self, validated_data):
        interfaces_dict = validated_data.pop('interface')
        validated_data['interface_id'] = interfaces_dict['id']
        return TestCases.objects.create(**validated_data)

    def put(self, instance, validated_data):
        if instance in validated_data:
            interfaces_dict = validated_data.pop('interfaces')
            validated_data['interfaces_id'] = interfaces_dict['id']
            instance.save()
        return super().update(instance, validated_data)


def whether_existed_env_id(value):
    """
    检查环境变量id是否存在
    """
    if value != 0:
        if not Envs.objects.filter(is_delete=False, id=value):
            raise serializers.ValidationError('环境变量不存在')


class TestcasesRunserializer(ModelSerializer):
    env_id = serializers.IntegerField(help_text="环境ID", validators=[whether_existed_env_id])

    class Meta:
        model = TestCases
        field = ('id', 'env_id')


