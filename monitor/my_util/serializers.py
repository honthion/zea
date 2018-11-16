from rest_framework import serializers
from monitor.my_util.response_util import ResponseData
import json, decimal
from decimal import Decimal


class ResponseDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResponseData
        fields = ('success', 'message', 'data')


#  use like this json.dumps({'x': decimal.Decimal('5.5')}, cls=DecimalEncoder)
class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


class fakefloat(float):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)


# Python JSON serialize a Decimal object
# https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
def defaultencode(o):
    if isinstance(o, Decimal):
        # Subclass float with custom repr?
        return fakefloat(o)
    raise TypeError(repr(o) + " is not JSON serializable")
