# models.py

from django.db import models


class RestAction (models.Model):
    
    name = models.CharField(max_length=10, blank=False, null=False, unique=True)
    description = models.CharField(max_length=10, blank=False, null=False)
    status = models.BooleanField()
    
    def __str__(self):
        
        return self.name
    
    class Meta:
        # Model metadata.
        db_table = 'manager_rest_action'  # Table name in the database
        verbose_name = 'rest_action'
        verbose_name_plural = 'rest_actions'


class Api (models.Model):
    
    action_id = models.ForeignKey(RestAction, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, null=False, blank=False)
    endpoint = models.CharField(max_length=255, null=False, blank=False)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        
        return f"{self.name} - {self.action_id.name}"
    
    class Meta:
        # Model metadata.
        db_table = 'manager_api'  # Table name in the database
        verbose_name = 'api'
        verbose_name_plural = 'apis'


class AddressIP (models.Model):
    
    address_ip = models.CharField(max_length=20, blank=False, null=False, unique=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.address_id
    
    class Meta:
        # Model metadata.
        db_table = 'manager_address_ip'  # Table name in the database
        verbose_name = 'address_ip'
        verbose_name_plural = 'address_ips'


class Status (models.Model):

    name = models.CharField(max_length=10, blank=False, null=False, unique=True)
    description = models.CharField(max_length=10, blank=False, null=False, unique=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
    class Meta:
        # Model metadata.
        db_table = 'manager_status'  # Table name in the database
        verbose_name = 'status'
        verbose_name_plural = 'status'

class Log (models.Model):
    
    addres_id = models.ForeignKey(AddressIP, on_delete=models.DO_NOTHING)
    api_id = models.ForeignKey(Api, on_delete=models.DO_NOTHING)
    status_id = models.ForeignKey(Status, default=1, on_delete=models.DO_NOTHING)
    consultation_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return f"{self.addres_id.address_ip} | {self.status_id.name} | ({self.consultation_date})"
    
    class Meta:
        # Model metadata.
        db_table = 'manager_log'  # Table name in the database
        verbose_name = 'log'
        verbose_name_plural = 'logs'