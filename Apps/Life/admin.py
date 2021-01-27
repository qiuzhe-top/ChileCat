from django.contrib import admin
from .models import (
    Room,Building,Floor,StuInRoom,
    RoomHistory,TaskRecord,Manage
)
# Register your models here.
@admin.register(Room)
class RoomTeleAdmin(admin.ModelAdmin):
    '''房间'''
    list_display = (
        "id","roomnum","floor","status"
        )
@admin.register(Building)
class BuildingTeleAdmin(admin.ModelAdmin):
    '''楼'''
    list_display = (
        "id","budnum"
        )
@admin.register(Floor)
class FloorTeleAdmin(admin.ModelAdmin):
    '''楼层'''
    list_display = (
        "id","budid","floornum"
        )
@admin.register(StuInRoom)
class StuInRommTeleAdmin(admin.ModelAdmin):
    '''房间学生信息'''
    list_display = (
        "id","roomid","stuid","status"
        )
@admin.register(RoomHistory)
class RoomHistoryTeleAdmin(admin.ModelAdmin):
    '''寝室访问记录'''
    list_display = (
        "id","roomid","managerid","createdtime"
        )
@admin.register(TaskRecord)
class TaskRecordTeleAdmin(admin.ModelAdmin):
    '''任务记录(被查)'''
    list_display = (
        "id","workerid","objstuid","reason","flag"
        ,"createdtime","lastmodifytime","buildingid",
        "managerid",
        )
@admin.register(Manage)
class ManageRecordTeleAdmin(admin.ModelAdmin):
    '''任务记录(被查)'''
    list_display = (
        "id","idcodetime","idcode","console"
        )
