"""
导入urls
"""
from django.urls import path
from . import views

urlpatterns = [
    # path('idcode', views.VerificationCode.as_view(), name='VerificationCode'),
    
    path('buildinginfo', views.BuildingInfo.as_view(), name='BuildingInfo'),
    path('roominfo', views.RoomInfo.as_view(), name='RoomInfo'),
    path('stupositioninfo', views.StudentPositionInfo.as_view(), name='StudentPositionInfo'),
    # path('studentleak', views.StudentLeak.as_view(), name='StudentLeak'),
    # path('recordsearch', views.RecordSearch.as_view(), name='RecordSearch'),
    # path('switchknowing', views.SwitchKnowing.as_view(), name='SwitchKnowing'),
    # path('exportexcel', views.ExportExcel.as_view(), name='ExportExcel'),
    # 学生晚查寝缺勤提交
    path('studentleak', views.StudentLeak.as_view(), name='StudentLeak'),
    # 记录查询返回所有缺勤记录
    path('recordsearch', views.RecordSearch.as_view(), name='RecordSearch'),
    # 导出excel
    path('exportexcel', views.ExportExcel.as_view(), name='ExportExcel'),

    
    # 任务
    path('task', views.Task.as_view(), name='Task'),
    # 添加管理员
    path('add_admin', views.AddAdmin.as_view(), name='AddAdmin'),
    # 任务开启
    path('switch', views.Switch.as_view(), name='Switch'),
    # 排班
    path('scheduling', views.Scheduling.as_view(), name='Scheduling'),
    # 查看考勤工作情况
    path('condition', views.Condition.as_view(), name='Condition'),
    # 查看考勤进度
    path('progress', views.Progress.as_view(), name='Progress'),
    # 销假
    path('undo_record', views.UndoRecord.as_view(), name='UndoRecord'),
    # 数据导出
    path('out_data', views.OutData.as_view(), name='OutData'),
    # 执行人获取任务
    path('task_executor', views.TaskExecutor.as_view(), name='TaskExecutor'),
    # 获取规则
    path('rule', views.Rule.as_view(), name='Rule'),
    
    # 获取学生信息
    path('student_information', views.student_information.as_view(), name='student_information'),
    # 考勤提交
    path('submit', views.submit.as_view(), name='submit'),
    # 执行人确认任务完成
    path('executor_finish', views.executor_finish.as_view(), name='executor_finish'),
    # 晚自修-管理的班级
    path('get_class', views.student_information.as_view(), name='student_information'),
    # 晚自修-班级内的学生
    path('class_students', views.student_information.as_view(), name='student_information'),
]
