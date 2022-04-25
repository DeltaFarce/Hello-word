from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from interfaces.models import Interfaces
from projects.models import Projects
from configures.models import Configures
from testcases.models import TestCases


class InterfacesModelSerializer(ModelSerializer):
    project_name = serializers.StringRelatedField(help_text="项目名称")
    project_id = serializers.PrimaryKeyRelatedField(help_text="项目ID", queryset=Projects.objects.all())

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'tester', 'desc', 'create_time', 'project_name', 'project_id')
        # read_only_fields = ['id', 'create_time', 'update_time']

    def create(self, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
        return super().update(instance, validated_data)


class InterfaceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class ConfiguresNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configures
        fields = ('id', 'name')


class TestCaseNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCases
        fields = ('id', 'name')


class InterfacesToConfiguresSerializer(serializers.ModelSerializer):
    configures = ConfiguresNameSerializer

    class Meta:
        model = Interfaces
        fields = ('id', 'configures')


class InterfacesToTestCasesSerializer(serializers.ModelSerializer):
    testcases = TestCaseNameSerializer

    class Meta:
        model = Interfaces
        fields = ('id', 'testcases')
