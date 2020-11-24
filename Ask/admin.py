'''
admin.py
'''
from django.contrib import admin
from .models import Ask,Audit

# Register your models here.
@admin.register(Ask)
class AskTeleAdmin(admin.ModelAdmin):
    '''
    请假条
    '''
    list_display = (
        "id","user_id","status","contact_info","ask_type","reason","place","ask_state",
        "start_time","end_time","created_time","modify_time","pass_id"
        )
@admin.register(Audit)
class AuditTeleAdmin(admin.ModelAdmin):
    '''
    审核
    '''
    list_display = ("id","user_id","ask_id","level","note","created_time","modify_time")
