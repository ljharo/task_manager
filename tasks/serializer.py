import re
import os
from datetime import datetime, timedelta
from rest_framework import serializers
from pydantic import ValidationError

from .schemas import CreateTaskSchema, CreateStepSchema
from .models import Task, Steps, Status


class CreateStepSerializer (serializers.Serializer):
    
    task_id = serializers.IntegerField()
    description = serializers.CharField(max_length=250)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    
    def create(self):
        step = Steps(**self.data)
        step.save()
        return {'result': 'the step was created successfully'}
    
    def validate(self, data):
        
        try:
            valid_data = CreateStepSchema(**data)
            date_now = datetime.now()
        except ValidationError as e:
            raise serializers.ValidationError(e)
        
        task_id = Task.objects.filter(id=valid_data.task_id).first()
        
        if task_id != None:
            if task_id.status_id == 2:
                raise serializers.ValidationError({'task_id':'You cannot assign a step to the task because it is already finished'})
        else:
            raise serializers.ValidationError({'task_id':'the task_id provided does not exist'})
        
        # validate step date and validate step date against task date
        if valid_data.start_date == None and valid_data.end_date != None:
            raise serializers.ValidationError({'date_error': 'you cannot define the date on which the step ends without first defining the date on which it begins'})
        
        if valid_data.start_date != None:
            if valid_data.start_date < date_now:
                raise serializers.ValidationError({'start_date': 'You cannot enter a date that is less than the current time'})

            if valid_data.start_date < task_id.start_date:
                raise serializers.ValidationError({'start_date': 'The time in which the step begins cannot be less than the time in which the task begins'})
                
        
        if valid_data.end_date != None:
            if valid_data.end_date <= date_now:
                raise serializers.ValidationError({'end_date': 'the end date cannot be less than or equal to the current time'})
            
            if valid_data.end_date > task_id.end_date:
                raise serializers.ValidationError({'end_date': 'The time in which the step is completed cannot be greater than the time in which the task is completed'})
        
        if valid_data.end_date <= valid_data.start_date:
            raise serializers.ValidationError({'date_error': 'The date on which the step ends cannot be less than the date on which it starts.'})
    

class CreateTaskSerializer (serializers.Serializer):
    
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    
    
    def create(self):
        
        if self.data['start_date'] == None and self.data['end_date']:
            
            self.data['start_date'] = datetime.now()
            self.data['end_date'] = self.data['start_date'] + timedelta(days=7)
        
        step = Task(**self.data)
        step.save()
        return {'result': 'the task was created successfully'}
    
    def validate(self, data):
        
        try:
            valid_data = CreateTaskSchema(**data)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        
        date_now = datetime.now()
        task = Task.objects.filter(title=valid_data.title).first()
        
        if task != None:
            raise serializers.ValidationError({'title': 'There is already a task with that title'})
        
        if valid_data.start_date == None and valid_data.end_date != None:
            raise serializers.ValidationError({'date_error': 'You cannot define the date on which the task will end without first having defined the date on which it begins.'})
        
        if valid_data.start_date != None:
            if valid_data.start_date < date_now:
                raise serializers.ValidationError({'start_date': 'You cannot enter a date that is less than the current time'})

        if valid_data.end_date != None:
            if valid_data.end_date <= date_now:
                raise serializers.ValidationError({'end_date': 'the end date cannot be less than or equal to the current time'})
        
        if valid_data.end_date <= valid_data.start_date:
            raise serializers.ValidationError({'date_error': 'The date on which the step ends cannot be less than the date on which it starts.'})
        
        return data