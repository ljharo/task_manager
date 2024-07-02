import os
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime


from .serializer import CreateStepSerializer, CreateTaskSerializer, UpdateTaskSerializer
from .models import Task

PORT = os.environ.get('PORT')
INTERNAL_KEY = os.environ.get('KEY_INTERNAL')
LOG_REGISTER_URL = f'http://localhost:{PORT}/manager/log/register/'
LOG_UPDATE_URL = f'http://localhost:{PORT}/manager/log/update/'

class TaskView (APIView):
    
    def get(self, request, id=None):
        pass
    
    def post(self, request) -> Response:
        
        data = {
            'internal_key': INTERNAL_KEY,
            'address_ip': request.META['REMOTE_ADDR'],
            'api_name': 'create_task',
            'method': request.method
        }
        response = requests.post(LOG_REGISTER_URL, json= data)
        
        if response.status_code == 200:
            log_id = response.json()['log_id']

        else: 
            return Response(response.json() ,status=400)

        serializer = CreateTaskSerializer(data=request.data)  # Crea un serializer con los datos de la solicitud
        
        if serializer.is_valid():  # Verifica si los datos son válidos
            
            result = serializer.create()
            result['log_id'] = log_id
            
            data2 = {
                'internal_key': INTERNAL_KEY,
                'log_id': log_id,
                'address_ip': request.META["REMOTE_ADDR"],
                'status_id': 2
            }
            requests.put(LOG_UPDATE_URL, json= data2)

            return Response(result, status=200)  # Devuelve la respuesta con los datos del conductor creado y un estado 201 (Created)
        
        else:
            data2 = {
                'internal_key': INTERNAL_KEY,
                'log_id': log_id,
                'address_ip': request.META["REMOTE_ADDR"],
                'status_id': 4
            }
            requests.put(LOG_UPDATE_URL, json= data2)
            
            return Response(serializer.errors, status=400)  # Devuelve la respuesta con los errores de validación y un estado 400 (Bad Request)

    def put(self, request):
        data = {
            'internal_key': INTERNAL_KEY,
            'address_ip': request.META['REMOTE_ADDR'],
            'api_name': 'put_tasks',
            'method': request.method
        }
        response = requests.post(LOG_REGISTER_URL, json= data)
        
        if response.status_code == 200:
            log_id = response.json()['log_id']

        else: 
            return Response(response.json() ,status=400)
    
        serializer = UpdateTaskSerializer(Task.objects.get(id=1), data=request.data, partial=True)  # Crea un serializer con los datos de la solicitud
        
        if serializer.is_valid():  # Verifica si los datos son válidos
            
            result = serializer.update(serializer.instance, serializer.validated_data)
            result['log_id'] = log_id
            
            data2 = {
                'internal_key': INTERNAL_KEY,
                'log_id': log_id,
                'address_ip': request.META["REMOTE_ADDR"],
                'status_id': 2
            }
            requests.put(LOG_UPDATE_URL, json= data2)

            return Response(result, status=200)  # Devuelve la respuesta con los datos del conductor creado y un estado 201 (Created)
        
        else:
            data2 = {
                'internal_key': INTERNAL_KEY,
                'log_id': log_id,
                'address_ip': request.META["REMOTE_ADDR"],
                'status_id': 4
            }
            requests.put(LOG_UPDATE_URL, json= data2)
            
            return Response(serializer.errors, status=400)  # Devuelve la respuesta con los errores de validación y un estado 400 (Bad Request)
    
    def delete(self, request, id):
        pass


class StepView (APIView):
    
    def get(self, request):
        pass
    
    def post(self, request):
        pass
    
    def put(self, request):
        pass
    
    def delete(self, request):
        pass