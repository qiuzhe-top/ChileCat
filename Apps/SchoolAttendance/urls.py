"""
导入urls
"""
from django.urls import path
from . import views

urlpatterns = [

    # 任务
    path('task', views.Task.as_view(), name='Task'),
    # 任务管理员
    path('task_admin', views.TaskAdmin.as_view(), name='TaskAdmin'),
    # 任务状态切换
    path('task_switch', views.TaskSwitch.as_view(), name='TaskSwitch'),
    # 排班
    path('scheduling', views.Scheduling.as_view(), name='Scheduling'),
    # 查看考勤工作情况
    path('condition', views.Condition.as_view(), name='Condition'),
    #     # 查看考勤执行进度
    #     path('progress', views.Progress.as_view(), name='Progress'),
    # 销假
    path('undo_record', views.UndoRecord.as_view(), name='UndoRecord'),
    # 数据导出
    path('out_data', views.OutData.as_view(), name='OutData'),


    # 执行人获取任务
    path('task_executor', views.TaskExecutor.as_view(), name='TaskExecutor'),
    # 获取规则
    path('rule', views.Rule.as_view(), name='Rule'),
    # 考勤提交  执行人确认任务完成
    path('submit', views.Submit.as_view(), name='Submit'),
    # 查寝相关任务信息 楼层 房间 学生状态
    path('task_room_info', views.TaskRoomInfo.as_view(), name='TaskRoomInfo'),


    # 晚自修-管理的班级  班级内的学生
    path('late_class', views.LateClass.as_view(),
         name='LateClass'),

    # 考勤记录查询接口 支持多条件查询
]