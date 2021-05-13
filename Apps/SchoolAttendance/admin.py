# from django.contrib import admin
# from .models import *
# # Register your models here.


# @admin.register(Room)
# class RoomTeleAdmin(admin.ModelAdmin):
#     """房间"""
#     list_display = (
#         "id", "name", "floor", "dorm_status", "health_status"
#     )


# @admin.register(Building)
# class BuildingTeleAdmin(admin.ModelAdmin):
#     """楼"""
#     list_display = (
#         "id", "name"
#     )


# @admin.register(Floor)
# class FloorTeleAdmin(admin.ModelAdmin):
#     """楼层"""
#     list_display = (
#         "id", "building", "name"
#     )


# @admin.register(StuInRoom)
# class StuInRoomTeleAdmin(admin.ModelAdmin):
#     """房间学生信息"""
#     list_display = (
#         "id", "room", "student", "status"
#     )


# @admin.register(RoomHistory)
# class RoomHistoryTeleAdmin(admin.ModelAdmin):
#     """寝室访问记录"""
#     list_display = (
#         "id", "room", "manager", "created_time"
#     )
# # @admin.register(TaskRecord)
# # class TaskRecordTeleAdmin(admin.ModelAdmin):
# #     """任务记录(被查)"""
# #     list_display = (
# #         "id", "worker", "student_approved", "reason"
# #         , "created_time", "last_modify_time", "manager",
# #     )
# #     # list_filter = ('reason', 'flag', 'created_time')
# #
# #
# # @admin.register(Manage)
# # class ManageRecordTeleAdmin(admin.ModelAdmin):
# #     """任务记录(被查)"""
# #     list_display = (
# #         "id", "generate_time", "verification_code", "console_code"
# #     )
# # @admin.register(PunishmentDetails)
# # class PunishmentDetailsTeleAdmin(admin.ModelAdmin):
# #     """规则一级分类"""
# #     list_display = (
# #         "id","name"
# #     )
# # @admin.register(PunishmentSort)
# # class PunishmentSortTeleAdmin(admin.ModelAdmin):
# #     """规则二级分类"""
# #     list_display = (
# #         "id","name","message"
# #     )


# @admin.register(Task)
# class ManageRecordTeleAdmin(admin.ModelAdmin):
#     """任务管理"""
#     list_display = (
#         "id", "college", "types", "generate_time", "verification_code", "console_code", "code_name"
#     )


# @admin.register(Rule)
# class Rule(admin.ModelAdmin):
#     """规则一级分类"""
#     list_display = (
#         "id", "name", "message"
#     )


# @admin.register(RuleDetails)
# class RuleDetails(admin.ModelAdmin):
#     """规则二级分类"""
#     list_display = (
#         "id", 'name', 'sort'
#     )


# @admin.register(Record)
# class Record(admin.ModelAdmin):
#     """任务记录"""
#     list_display = (
#         "id", "task_type", "worker", "student_approved", "manager", "task_type", "score",
#         "reason_str", "created_time", "last_modify_time", "room_str", "grade_str"
#     )
