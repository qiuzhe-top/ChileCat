from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(TeacherForCollege)
class TeacherForCollege(admin.ModelAdmin):
    list_display = (
        "id", "user"
    )


@admin.register(Grade)
class Grade(admin.ModelAdmin):
    list_display = (
        "id", "name", "college", "whole_grade"
    )


@admin.register(WholeGrade)
class WholeGrade(admin.ModelAdmin):
    list_display = (
        "id", "user", "name"
    )


@admin.register(College)
class College(admin.ModelAdmin):
    list_display = (
        "id", "name", "code_name"
    )


@admin.register(Building)
class Building(admin.ModelAdmin):
    list_display = (
        "id", "name"
    )


@admin.register(Floor)
class Floor(admin.ModelAdmin):
    list_display = (
        "id", "name", "building"
    )


@admin.register(Room)
class Room(admin.ModelAdmin):
    list_display = (
        "id", "name", "floor", "health_status", "dorm_status"
    )


@admin.register(StuInRoom)
class StuInRoom(admin.ModelAdmin):
    list_display = (
        "id", "room", "student", "bed_position" #, "status"
    )
