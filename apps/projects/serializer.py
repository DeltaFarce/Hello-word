from rest_framework import serializers
from interfaces.models import Interfaces
from projects.models import Projects


class ProjectsModelSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(label='Id主键', help_text='Id主键', read_only=True)
    name = serializers.CharField(label='项目名称', max_length=200, help_text='项目名称')
    leader = serializers.CharField(label='负责人', max_length=200, help_text='负责人')
    tester = serializers.CharField(label='测试人', max_length=200, help_text='测试人')
    programer = serializers.CharField(label='开发人', max_length=200, help_text='开发人')
    publish_app = serializers.CharField(label='发布应用', max_length=200, help_text='发布应用')
    create_time = serializers.CharField(label='创建时间', help_text='创建时间', read_only=True)
    update_time = serializers.CharField(label='更新时间', help_text='更新时间', read_only=True)
    is_delete = serializers.BooleanField(default=False, label='逻辑删除', help_text='逻辑删除')
    desc = serializers.CharField(label='描述', help_text='描述', default='')

    def create(self, validated_data):
        instance = Projects.objects.create(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.leader = validated_data.get('leader')
        instance.tester = validated_data.get('tester')
        instance.programer = validated_data.get('programer')
        instance.publish_app = validated_data.get('publish_app')
        instance.desc = validated_data.get('desc')
        instance.save()
        return instance


class InterfacesName(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class ProjectsToInterfaces(serializers.ModelSerializer):
    interfaces = InterfacesName(read_only=True, many=True)

    class Meta:
        model = Projects
        fields = ('id', 'name', 'leader', 'tester', 'programer', 'publish_app', 'create_time', 'update_time',
                  'is_delete', 'desc', 'interfaces')


class InterfaceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'tester')


class InterfacesByProjectSerializer(serializers.ModelSerializer):
    interfaces = InterfaceNameSerializer(many=True)

    class Meta:
        model = Projects
        fields = ('id', 'interfaces')
