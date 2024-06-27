from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterLogSerializer, UpdateLogSerializer

class LogView (APIView):
    
    def post(self, request) -> Response:
        serializer = RegisterLogSerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.create()
            return Response(result, status=200)
        
        else:
            return Response(serializer.errors, status= 400)
    
    def put(self, request) -> Response:
        
        serializer = UpdateLogSerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.create()
            return Response(result, status=200)
        
        else:
            return Response(serializer.errors, status= 400)