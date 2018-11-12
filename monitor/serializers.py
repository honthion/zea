from rest_framework import serializers
from monitor.models import Item
from django.contrib.auth.models import User

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = (
        'id', 'ctime', 'utime', 'mon_title', 'mon_type', 'mon_trigger', 'mon_trigger_desc', 'mon_desc', 'mon_status')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'snippets', 'password')
