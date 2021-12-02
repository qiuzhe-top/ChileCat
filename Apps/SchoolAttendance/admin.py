'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-12-01 20:11:28
Description: 
'''
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import *
from django.utils.html import format_html

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """任务管理"""
    list_display = (
        "id", "college", "types", "is_open"
    )
    filter_horizontal = ("admin","buildings","grades")



class CountryFilter(SimpleListFilter):
    title = '是否查询销假人' # or use _('country') for translated title
    parameter_name = '是否查询销假人'

    def lookups(self, request, model_admin):
        return [(1, '否'), (2, '是')]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            return queryset.filter(manager__isnull=True)
        elif value == '2':
            return queryset.filter(manager__isnull=False)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """考勤记录"""
    list_display = (
        "id", "task","rule_str","score","grade_str","room_str",
        "student_approved","student_approved_name","worker",
        "worker_name","manager","manager_name", "star_time","last_time",
    )
    list_filter = ("rule__rule__name","rule__name","grade_str",CountryFilter)
    # list_editable =("rule_str","score")
    date_hierarchy = 'star_time'

    search_fields = ("student_approved__username","student_approved__name","manager__username","manager__name")
    actions = ['batch_pin','batch_pin_cancel' ]

    def batch_pin(self, request, queryset):
        flag = True
        for i in queryset:
            if i.manager:
                self.message_user(request, '已经有人被销假了，无法批量销假！！')
                flag = False
                break
            else:
                continue
        if flag:
            for q in queryset:
                q.manager  = request.user
                q.save()
            self.message_user(request, '批量销假成功！！')

    batch_pin.short_description = '批量销假'

    def batch_pin_cancel(self, request, queryset):
        if request.user:
            queryset.update(manager = None,manager_username=None,manager_name=None)
            self.message_user(request, '批量销假成功！！')

    batch_pin_cancel.short_description = '批量取消销假'

    def  student_approved_name(self,obj):
        try:
            return obj.student_approved.name
        except:
            return None
    student_approved_name.short_description = '被执行者姓名'

    def worker_name(self,obj):
        try:
            return obj.worker.name
        except:
            return None
    worker_name.short_description = '执行者姓名'
    
    def manager_name(self,obj):
        try:
            return obj.manager.name
        except:
            return None
    manager_name.short_description = '销假人姓名'
    # # 添加自定义按钮
    # def operator(self, obj):
    #     return format_html(
    #     '<a href="/api/school_attendance/undo/record/">更新<a/>'
    #     )
    # operator.short_description = '数据更新'
@admin.register(RuleDetails)
class RuleDetailsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name","score","rule","parent_id"
    )
