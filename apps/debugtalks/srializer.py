from debugtalks.models import Debugtalks
from rest_framework.serializers import ModelSerializer


class DebugtalksModelSerializer(ModelSerializer):
    class Meta:
        model = Debugtalks
        fields = '__all__'
        read_only_fields = ('name', 'project')

        # extra_kwargs = {
        #     'debugtalk': {
        #         'write_only': True
        #     }
        # }