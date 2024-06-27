from django.db import models


class Status (models.Model):

    name = models.CharField(max_length=10, blank=False, null=False, unique=True)
    description = models.CharField(max_length=10, blank=False, null=False, unique=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
    class Meta:
        # Model metadata.
        db_table = 'task_status'  # Table name in the database
        verbose_name = 'status'
        verbose_name_plural = 'status'


class Task (models.Model):
    
    status_id = models.ForeignKey(Status, default='1', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.CharField(max_length=500, blank=False, null=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def __str__(self):
        
        return self.title
    
    class Meta:
        # Model metadata.
        db_table = 'task'  # Table name in the database
        verbose_name = 'task'
        verbose_name_plural = 'tasks'


class Steps (models.Model):
    
    id_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=False, null=False)
    status = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    
    def __str__(self):
        
        return self.id_task.title
    
    class Meta:
        # Model metadata.
        db_table = 'task_steps'  # Table name in the database
        verbose_name = 'task_steps'
        verbose_name_plural = 'task_steps'
