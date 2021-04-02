from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Manage)
class ManageRecordTeleAdmin(admin.ModelAdmin):
    """任务管理"""
    list_display = (
        "id", "college","types", "generate_time", "verification_code", "console_code", "code_name"
    )


@admin.register(PunishmentSort)
class PunishmentSortTeleAdmin(admin.ModelAdmin):
    """规则一级分类"""
    list_display = (
        "id", "name", "message"
    )


@admin.register(Punishment)
class TaskRecordTeleAdmin(admin.ModelAdmin):
    """规则二级分类"""
    list_display = (
        "id", 'name', 'sort'
    )


@admin.register(PunishmentDetails)
class PunishmentDetailsTeleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "score", "is_person", "punishment"
    )


@admin.register(TaskRecord)
class TaskRecordTeleAdmin(admin.ModelAdmin):
    """任务记录"""
    list_display = (
        "id", "task_type", "worker", "student_approved", "manager", "task_type", "score",
        "reason_str", "created_time", "last_modify_time", "room_str", "grade_str"
    )
