from django.contrib import admin
from .models import *


@admin.register(UserCall)
class UserCall(admin.ModelAdmin):
    """楼层"""
    list_display = (
        "id", "task", "user", "rule"
    )


@admin.register(TaskFloorStudent)
class TaskFloorStudent(admin.ModelAdmin):
    """房间学生信息"""
    list_display = (
        "id", "task", "user", "flg"
    )


@admin.register(RoomHistory)
class RoomHistoryTeleAdmin(admin.ModelAdmin):
    """寝室访问记录"""
    list_display = (
        "id", "room", "task", "created_time"
    )


# @admin.register(TaskClass)
# class TaskClass(admin.ModelAdmin):
#     list_display = (
#         "id", "task", "grade"
#     )


# @admin.register(TaskFloor)
# class TaskFloor(admin.ModelAdmin):
#     list_display = (
#         "id", "task", "building"
#     )


@admin.register(TaskPlayer)
class TaskPlayer(admin.ModelAdmin):
    list_display = (
        "id", "task", "user", "is_admin"
    )


@admin.register(Task)
class Task(admin.ModelAdmin):
    """任务管理"""
    list_display = (
        "id", "user", "is_open", "types", "user"
    )
    raw_id_fields = ['user',]

    filter_horizontal=['grades',]


@admin.register(Rule)
class Rule(admin.ModelAdmin):
    """规则一级分类"""
    list_display = (
        "id", "name", "message"
    )


@admin.register(RuleDetails)
class RuleDetails(admin.ModelAdmin):
    """规则二级分类"""
    list_display = (
        "id", 'name', 'score'
    )


@admin.register(Record)
class Record(admin.ModelAdmin):
    """任务记录"""
    list_display = (
        "id", "task", "rule", "rule_str", "score","grade_str","student_approved","worker","manager","star_time","last_time"
    )
