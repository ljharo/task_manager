import os
from rest_framework import serializers
from pydantic import ValidationError
from datetime import datetime

from .models import Log, Api, AddressIP, Status
from .schema import RegisterLogSchema, UpdateLogSchema

INTERNAL_KEY = os.environ.get('KEY_INTERNAL')

class RegisterLogSerializer (serializers.Serializer):
    
    internal_key = serializers.CharField(max_length=100)
    address_ip = serializers.CharField(max_length=20)
    api_name = serializers.CharField(max_length=255)
    method = serializers.CharField(max_length=10)
    
    def create(self):
        
        validated_data = self.data
        
        addres_id = AddressIP.objects.filter(address_ip=validated_data['address_ip']).first()
        api_id = Api.objects.filter(name=validated_data['api_name']).first()
        
        log = Log(addres_id=addres_id, api_id=api_id)
        log.save()

        result = {
            'log_id': log.id
        }        
        
        return result
    
    def validate(self, data):
        
        try: 
            valid_data = RegisterLogSchema(**data)
            
            # internal_key validatiom
            if valid_data.internal_key != INTERNAL_KEY:
                raise serializers.ValidationError({'internal_key':'The internal key is not correct'})
            
            #  validation
            address_ip, created  = AddressIP.objects.get_or_create(address_ip=valid_data.address_ip)
            
            if not created:
                if not address_ip.status:
                    raise serializers.ValidationError({'addres_id': 'The IP address does not have permission to use the API.'})
            
            # api_name avlid
            valid_api = Api.objects.filter(name= valid_data.api_name).first()
            if valid_api:
                if not valid_api.status:
                    raise serializers.ValidationError({'api_name': 'the api is currently not enabled'})
            else:
                raise serializers.ValidationError({'api_name': 'the api does not exist'})
                
            # method valid
            if valid_data.method != valid_api.action_id.name:
                raise serializers.ValidationError({'method':'The method with which you are consulting the API is not the correct one'})
            
        except ValidationError as e:
            raise serializers.ValidationError(e)
        
        return data

class UpdateLogSerializer (serializers.Serializer):
    
    log_id = serializers.IntegerField()
    status_id = serializers.IntegerField()
    address_ip = serializers.CharField(max_length=20)
    internal_key = serializers.CharField(max_length=100)
    
    def create(self):
        
        validated_data = self.data
        log = Log.objects.filter(id=validated_data['log_id']).first()
        log.status_id = Status.objects.filter(id=validated_data['status_id']).first()
        log.save()
        
        return {'status':'the log status has just been updated'}
    
    def validate(self, data):
        
        try:
            valid_data = UpdateLogSchema(**data)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        
        if valid_data.internal_key != INTERNAL_KEY:
            raise serializers.ValidationError({'internal_key':'The internal key is not correct'})
        
        address_ip = AddressIP.objects.filter(address_ip= valid_data.address_ip).first()
        
        if address_ip != None:
            if not address_ip.status:
                raise serializers.ValidationError({'addres_id': 'The IP address does not have permission to use the API.'})
        else:
            raise serializers.ValidationError({'addres_id': 'The address is not registered, you cannot update the status.'})
        
        if not Log.objects.filter(id=valid_data.log_id).exists():
            raise serializers.ValidationError({'The log with the given ID does not exist'})
        
        status_id = Status.objects.filter(id=valid_data.status_id).first()

        if status_id != None:
            if not status_id.status:
                raise serializers.ValidationError({'status_id': 'This status is not allowed at this time'}) 
        else:
            raise serializers.ValidationError({'status_id': 'The status with the given ID does not exist'}) 
        
        return data