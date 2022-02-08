# '''
# Author: 邹洋
# Date: 2022-01-26 13:52:02
# Email: 2810201146@qq.com
# LastEditors:  
# LastEditTime: 2022-02-07 10:29:06
# Description:  考勤的工作人员，业务部分
# ''' 
# import json

# from Apps.SchoolAttendance.models import *
# from Apps.SchoolAttendance.views.parent import *
# from Apps.SchoolInformation.common.configuration import *
# from Apps.SchoolInformation.models import *
# from Apps.SchoolInformation.serializers import *
# from cool.views import CoolAPIException, ErrorCode, ViewSite
# from Core.views import *
# from django.utils.translation import gettext_lazy as _
# from django_redis import get_redis_connection
# from rest_framework import fields

# from .admin import *

# site = ViewSite(name='Worker', app_name='Worker')

# # ================================================= #
# # ************** 晚查寝 相关功能      ************** #
# # ================================================= #

# @site
# class DormStudentRoomInfo(TaskBase):
#     name = _('房间学生 列表')

#     def get_context(self, request, *args, **kwargs):
#         self.get_task()
#         room_id = request.params.room_id
#         dorm = -1#DormCallCache()
#         stus = dorm.get_room_stu(room_id)
#         # types = dorm.get_type_by_dorm_key(self.task.types)
#         stu_status = []
#         for s in stus:
#             stus[s]['status'] = 1
#             # stu_status.append(stus[s]['room']+"_"+types+"_"+s)
#             stus[s]['id'] = s
#         return stus.values()

#     class Meta:
#         param_fields = (('room_id', fields.CharField(label=_('房间ID'))),)


# @site
# class SubmitKnowing(SubmitBase):
#     name = _('寝室考勤 点名提交')

#     def get_custom_rule(self):
#         '''获取自定义规则'''
#         return create_custom_rule(RULE_CODE_01, RULE_NAME_01_01)

#     def updata_user_in_room(self, record_model, is_flg):
#         '''修改学生在宿舍情况'''
#         dorm = DormCallCache()
#         room = record_model['room_str']
#         username = record_model['student_approved_username']
#         if is_flg == False:
#             flg = dorm.get_stu_status(self.task.types,username)
#             # 如果状态为不在寝室 就不进行提交
#             if int(flg) == 0:
#                 return False
#             else:
#                 dorm.set_stu_status(room,self.task.types,username,0)
#         elif is_flg == True:
#             dorm.set_stu_status(room,self.task.types,username,1)

#     def submit_undo_record(self,record_model, user):
#         self.updata_user_in_room(record_model, True)
#         record_model['rule_str'] = '查寝：误操作撤销'

#         # 通过记录时间、任务、学生信息 定位考勤记录信息
#         start_date = get_start_date(self.request)
#         end_date = get_end_date(self.request)
#         records = models.Record.objects.filter(
#             task=self.task,
#             student_approved_username=record_model['student_approved_username'],
#             student_approved_name=record_model['student_approved_name'],
#             star_time__range=(start_date,end_date),
#         )

#         for record in records:
#             username = record_model['manager'].username
#             name = record_model['manager'].name
#             self.undo_record(record, username, name)

#     def submit_check(self, record_model, record):
#         '''提交学生考勤记录'''
#         return self.updata_user_in_room(record_model, False)

#     class Meta:
#         param_fields = (('room_id', fields.CharField(label=_('房间ID'))),)




# # ================================================= #
# # ************** 晚自修 相关功能      ************** #
# # ================================================= #


# @site
# class LateClass(TaskBase, UserCallCache):
#     name = _('获取班级点名名单')

#     def get_grades(self):
#         # TODO 修改前端 使用数组进行处理
#         grades_list = self.task.get_grades()
#         data = []
#         for g in grades_list:
#             data.append({"id": g, "name": g})
#         return data

#     def get_grade_all_call(self, grade, task_id):
#         '''
#         获取班级点名数据,缓存7天

#         Args:
#             grade (班级): 班级编号或者ID
#             task_id (任务ID): 当前点名任务的ID
#         '''

#     # TODO 添加清除所有班级点名名单缓存 初始化所有点名名单信息

#     def get_grade_student(self, request):
#         '''
#         获取班级名单包含点名状态

#         Args:
#             request ([type]): [description]
#         '''
#         class_id = request.params.class_id
#         rule_id = request.params.rule_id

#         # 获取班级所有学号
#         call = self.init_cache().get_grade_call(class_id)
        
#         for c in call.values():
#             c['flg'] = c[rule_id] if rule_id in c.keys() else None
#         return call.values()

#     def get_context(self, request, *args, **kwargs):
#         self.get_task_player_by_user()
#         type_ = int(request.params.type)
#         if type_ == 0:
#             return self.get_grades()
#         elif type_ == 1:
#             return self.get_grade_student(request)

#     class Meta:
#         param_fields = (
#             ('rule_id', fields.CharField(label=_('规则ID'), default=None)),
#             ('class_id', fields.CharField(label=_('班级ID'), default=None)),
#             (
#                 'type',
#                 fields.CharField(
#                     label=_('类型'), help_text="0 # 获取任务绑定的班级 1 # 获取班级名单附带学生多次点名情况"
#                 ),
#             ),
#         )


# @site
# class SubmitLateDiscipline(SubmitBase):
#     name = _('晚自修违纪提交')

#     def get_custom_rule(self):
#         '''获取自定义规则'''
#         return create_custom_rule(RULE_CODE_03, RULE_NAME_03_01)

#     def submit_check(self, record_model, record):
#         '''提交学生考勤记录'''
#         if record['reason_is_custom']:
#             if len(record_model['rule_str']) <= 0:
#                 raise CoolAPIException(ErrorCode.THE_REASON_IS_EMPTY)

#             score = int(record_model['score'])
#             if score <= 0 or score > 10:
#                 raise CoolAPIException(ErrorCode.CUSTOM_SCORE_ERROR)

#             record_model['score'] = record['score']


# @site
# class SubmitLate(SubmitBase):
#     name = _('晚自修点名提交')

#     def submit_check(self, record_model, record):
#         '''提交学生考勤记录'''
#         cache = get_redis_connection()
#         call = cache.hget(LateClass.KEY_SPACE, record['grade'])
#         call = json.loads(call)
#         user_call = call[record['user_id']]

#         # 判断是不是本次任务第一次点名
#         rule_id = str(record['reason'])
#         if rule_id in user_call.keys():
#             is_save = user_call[rule_id] == None
#         else:
#             is_save = True

#         if is_save:
#             user_call[rule_id] = self.request.params.flg
#             cache.hset(LateClass.KEY_SPACE, record['grade'], json.dumps(call))
#             return not self.request.params.flg

#         return is_save

#     class Meta:
#         param_fields = (('flg', fields.BooleanField(label=_('点名 在/不在'))),)


# # ================================================= #
# # ************** 寝室卫生 相关功能      ************** #
# # ================================================= #


# @site
# class SubmitHealth(SubmitBase):
#     name = _('寝室卫生 检查提交')

#     def get_custom_rule(self):
#         '''获取自定义宿舍卫生规则'''
#         return create_custom_rule(RULE_CODE_07, RULE_NAME_07_01)

#     def submit_check(self, record_model, record):
#         '''提交学生考勤记录'''
#         pass

#     class Meta:
#         param_fields = (('room_id', fields.CharField(label=_('房间ID'))),)




# worker_urls = site.urls
# worker_urlpatterns = site.urlpatterns
