from django.contrib import admin
from .models import (
    Room, Building, Floor, StuInRoom,
    RoomHistory, TaskRecord, Manage
)


# Register your models here.
@admin.register(Room)
class RoomTeleAdmin(admin.ModelAdmin):
    """房间"""
    list_display = (
        "id", "name", "floor", "status"
    )


@admin.register(Building)
class BuildingTeleAdmin(admin.ModelAdmin):
    """楼"""
    list_display = (
        "id", "name"
    )


@admin.register(Floor)
class FloorTeleAdmin(admin.ModelAdmin):
    """楼层"""
    list_display = (
        "id", "building", "name"
    )


@admin.register(StuInRoom)
class StuInRoomTeleAdmin(admin.ModelAdmin):
    """房间学生信息"""
    list_display = (
        "id", "room", "student", "status"
    )


@admin.register(RoomHistory)
class RoomHistoryTeleAdmin(admin.ModelAdmin):
    """寝室访问记录"""
    list_display = (
        "id", "room", "manager", "created_time"
    )


@admin.register(TaskRecord)
class TaskRecordTeleAdmin(admin.ModelAdmin):
    """任务记录(被查)"""
    list_display = (
        "id", "worker", "student_approved", "reason", "flag"
        , "created_time", "last_modify_time", "manager",
    )


@admin.register(Manage)
class ManageRecordTeleAdmin(admin.ModelAdmin):
    """任务记录(被查)"""
    list_display = (
        "id", "generate_time", "verification_code", "console_code"
    )
