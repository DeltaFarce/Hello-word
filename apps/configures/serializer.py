from rest_framework import serializers
from configures.models import Configures
from interfaces.models import Interfaces
from projects.models import Projects


class InterfacesAnotherSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text="项目名称")
    id = serializers.IntegerField(help_text="接口ID")
    project_id = serializers.PrimaryKeyRelatedField(help_text="项目ID", queryset=Projects.objects.all())

    class Meta:
        model = Interfaces
        fields = ('name', 'project', 'id', 'project_id')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validated(self, attrs):
        """校验项目id是否与接口ID一致"""
        if not Interfaces.objects.filter(id=attrs['id'], project_id=attrs['project_id'], is_delete=False):
            raise serializers.ValidationError('项目和接口信息不对应')
        return attrs


class ConfiguresSerializer(serializers.ModelSerializer):
    """ 配置序列化器 """

    interfaces = InterfacesAnotherSerializer(help_text="项目ID和接口ID")

    class Meta:
        model = Configures
        fields = ('id', 'name', 'author', 'request', 'interfaces')

        # extra_kwargs = {
        #     'request': {
        #         'write_only': True
        #     }
        # }

    def create(self, validated_data):
        interfaces_dict = validated_data.pop('interfaces')
        validated_data['interfaces_id'] = interfaces_dict['id']
        return Configures.objects.create(**validated_data)

    def put(self, instance, validated_data):
        if instance in validated_data:
            interfaces_dict = validated_data.pop('interfaces')
            validated_data['interfaces_id'] = interfaces_dict['id']
            instance.save()
        return super().update(instance, validated_data)