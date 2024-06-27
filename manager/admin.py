# admin.py

from django.contrib import admin
from .models import RestAction, Api, AddressIP, Status, Log

class LogAdmin(admin.ModelAdmin):
    list_display = ('addres_id', 'api_id', 'consultation_date')
    list_filter = ('consultation_date',)
    ordering = ('-consultation_date',)  # Ordenar por fecha de registro descendente

admin.site.register(RestAction)
admin.site.register(Api)
admin.site.register(AddressIP)
admin.site.register(Status)
admin.site.register(Log, LogAdmin)