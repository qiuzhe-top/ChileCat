"""
admin.py
"""
from django.contrib import admin
from .models import Ask, Audit, AskType, ASK_TYPE


@admin.register(Ask)
class AskTeleAdmin(admin.ModelAdmin):
    """
    请假条
    """
    list_display = (
        "id", "user_id", "status", "contact_info", "ask_type", "reason", "place", "ask_state",
        "start_time", "end_time", "extra_end_time", "created_time", "modify_time", "grade_id", "pass_id"
    )


@admin.register(Audit)
class AuditTeleAdmin(admin.ModelAdmin):
    """
    审核
    """
    list_display = ("id", "user_id", "ask_id", "status", "created_time", "modify_time")


@admin.register(AskType)
class AskTypeTeleAdmin(admin.ModelAdmin):
    """
    请假类别
    """
    list_display = ("id", "type_name")
