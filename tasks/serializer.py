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


# Task
class CreateTaskSerializer (serializers.Serializer):
    
    current_time = datetime.now()
    
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    start_date = serializers.DateTimeField(default=current_time)
    end_date = serializers.DateTimeField(default=(current_time + timedelta(days=7)))
    
    
    def create(self):
        
        # self.data['start_date'] = self.data['start_date'].strftime("%Y-%m-%d")
        # self.data['end_date'] = self.data['end_date'].strftime("%Y-%m-%d")
    
        task = Task(**self.data)
        task.save()
        
        result = {
            'task_id': task.id,
            'result': 'the task was created successfully'
        }
        
        return result
    
    def validate(self, data):
        
        try:
            valid_data = CreateTaskSchema(**data)
            
            # acomodamos el formato de las fechas
            valid_data.start_date = valid_data.start_date.replace(tzinfo=None)
            valid_data.end_date = valid_data.end_date.replace(tzinfo=None)
            
        except ValidationError as e:
            raise serializers.ValidationError(e)
        
        date_now = datetime.now()
        task = Task.objects.filter(title=valid_data.title).first()
        
        if task != None:
            raise serializers.ValidationError({'title': 'There is already a task with that title'})
        
        if valid_data.start_date == None and valid_data.end_date != None:
            raise serializers.ValidationError({'date_error': 'You cannot define the date on which the task will end without first having defined the date on which it begins.'})
        if valid_data.start_date != None and valid_data.end_date == None:
            raise serializers.ValidationError({'date_error': 'you have to define the date on which the task will be completed.'})
        
        # if valid_data.start_date != None:
        #     if valid_data.start_date <= date_now:
        #         raise serializers.ValidationError({'start_date': 'You cannot enter a date that is less than the current time'})

        # if valid_data.end_date != None:
        #     if valid_data.end_date <= date_now:
        #         raise serializers.ValidationError({'end_date': 'the end date cannot be less than or equal to the current time'})
        
        if valid_data.end_date < valid_data.start_date:
            raise serializers.ValidationError({'date_error': 'The date on which the task ends cannot be less than the date on which it starts.'})
        
        return data


class UpdateTaskSerializer(serializers.Serializer):
    
    current_time = datetime.now()
    
    task_id = serializers.IntegerField()
    title = serializers.CharField(max_length=100, default=None)
    description = serializers.CharField(max_length=500, default=None)
    start_date = serializers.DateTimeField(default=None)
    end_date = serializers.DateTimeField(default=None)
    
    def create(self):
        
        data = self.data
        task = Task.objects.filter(id=data['task_id']).first()
        
        if data['title'] != None:
            task.title = data['title']
        
        if data['description'] != None:
            task.description = data['description']
        
        if data['start_date'] != None:
            task.start_date = data['start_date']
        
        if data['end_date'] != None:
            task.end_date = data['end_date']
        
        task.save()
        
        result = {
            'task_id': task.id,
            'result': 'the task was update successfully'
        }
        
        return result
    
    def validate(self, data):
        
        task = Task.objects.filter(id=data['task_id']).first()

        if task == None:
            raise serializers.ValidationError({'task_id': 'the task_id does not exist'})
        
        data_copy = data.copy()
        del data_copy['task_id']
        
        if data['title'] != None:
            
            if data['title'] == task.title:
                data['tittle'] = None
            else:
                title = Task.objects.filter(title=data['title']).first()
                if title != None:
                    if title.id != task.id:
                        raise serializers.ValidationError({'title': 'There is already a task that contains that title'})
        
        start_date = datetime(data['start_date']) if data['start_date'] == None else data['start_date']
        end_date = datetime(data['end_date']) if data['end_date'] == None else data['end_date']
        
        if start_date != None and  end_date != None:
            if start_date > end_date:
                raise serializers.ValidationError({'date_error': 'The date on which the race begins cannot be greater than the date on which it ends.'})

        if start_date != None and  end_date == None:
            if start_date > task.end_date:
                raise serializers.ValidationError({'date_error': 'The date on which the race begins cannot be greater than the date on which it ends.'})
        
        if start_date == None and  end_date != None:
            if end_date > task.start_date:
                raise serializers.ValidationError({'date_error': 'The date on which the task is completed cannot be less than the date on which it begins.'})
        
        if any(data_copy.items()):
            raise serializers.ValidationError({"fields":"you have to enter values ​​to be able to update"})
            
        return data
