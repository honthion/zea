from rest_framework import serializers
from monitor.my_util.response_util import ResponseData


class ResponseDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResponseData
        fields = ('success', 'message', 'data')
