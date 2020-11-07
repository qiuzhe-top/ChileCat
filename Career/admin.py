'''
admin.py
'''
from django.contrib import admin
from .models import Career

@admin.register(Career)
class CareerTeleAdmin(admin.ModelAdmin):
    '''
    职业
    '''
    list_display = ("id","title","note","text","source","viewnum","release_time")
