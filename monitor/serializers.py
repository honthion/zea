from rest_framework import serializers
from monitor.models import Item


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = (
        'id', 'ctime', 'utime', 'mon_title', 'mon_type', 'mon_trigger', 'mon_trigger_desc', 'mon_desc', 'mon_status')
