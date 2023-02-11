from rest_framework.response import Response
from rest_framework import status

def response_success(message,data,status):
    return Response({
        'message': message,
        'status_code' : status,
        'data' : data
    }, status=status)

def response_error(message,error,status):
    return Response({
        'message': message,
        'status_code' : status,
        'error' : error
    }, status=status)