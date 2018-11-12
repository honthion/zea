import json
from django.http import JsonResponse
from django.core import serializers
from restless.models import serialize


class ResponseData():
    def __init__(self, success, message, data):
        self.success = success
        self.message = message
        self.data = data



@staticmethod
def getSuccess():
    responseData = ResponseData(True, "", "")
    return JsonResponse(responseData, safe=False)

@staticmethod
def dataSuccess(data):
    responseData = ResponseData(True, "", data)
    return serialize(responseData)

@staticmethod
def getError():
    return JsonResponse({"success": False, "msg": "", "data": ""})
