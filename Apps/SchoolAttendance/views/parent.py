# '''
# Author: 邹洋
# Date: 2022-02-07 10:09:45
# Email: 2810201146@qq.com
# LastEditors:  
# LastEditTime: 2022-02-07 10:33:21
# Description: 父级视图
# '''
# import json

# from django.http import JsonResponse

# from Apps.SchoolAttendance.models import *
# from Apps.SchoolInformation.models import *
# from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, utils
# from cool.views.exceptions import CoolAPIException
# from Core.views import *
# from Core.views import PermissionView
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
# from rest_framework import fields, utils

# User = get_user_model()


# class TaskBase(PermissionView):
#     def get_context(self, request, *args, **kwargs):
#         raise NotImplementedError

#     def is_open(self):
#         if not self.task.is_open:
#             raise CoolAPIException(ErrorCode.ERR_TASK_ISOPEN_FALSE)

#     def get_task(self):
#         '''通过任务id获取任务'''
#         try:
#             id = self.request.params.task_id
#             self.task = Task.objects.get(id=int(id))
#             self.request.task = self.task
#             return self.task
#         except:
#             raise CoolAPIException(ErrorCode.ERR_TAKS_NO_TASK)

#     def get_task_by_user(self):
#         '''通过管理用户和任务id获取任务'''
#         try:
#             id = self.request.params.task_id
#             username = self.request.user.username
#             self.task = Task.objects.get(id=int(id))
#             if username in self.task.get_admin():
#                 self.request.task = self.task
#                 return self.task
#             else:
#                 raise CoolAPIException(ErrorCode.ERR_TAKS_USER_HAS_NO_TASK)
#         except:
#             raise CoolAPIException(ErrorCode.ERR_TAKS_NO_TASK)

#     def get_task_player_by_user(self):
#         '''通过工作用户和任务id获取任务'''
#         try:
#             id = self.request.params.task_id
#             username = self.request.user.username
#             self.task = TaskPlayer.objects.get(task=int(id), username=username).task
#             self.request.task = self.task
#             return self.task
#         except:
#             raise CoolAPIException(ErrorCode.ERR_TAKS_USER_HAS_NO_TASK)

#     def init_scheduling(self, users, roster):
#         '''初始化班表'''
#         self.get_task_by_user()

#         # 历史班表清空
#         TaskPlayer.objects.filter(task=self.task).delete()

#         # 新用户进行任务绑定
#         for username in users:
#             TaskPlayer.objects.get_or_create(task=self.task, username=username)


#         self.task.roster = json.dumps(roster)
#         self.task.save()

#     class Meta:
#         param_fields = (('task_id', fields.CharField(label=_('任务id'), max_length=8)),)
#         path = '/'


# class RecordBase:
#     def init_custom_rule(self):
#         '''
#         构建规则（自定义）

#         Returns
#         -------
#         models.Rule
#             规则实例
#         '''
#         if self.custom_rule:
#             return self.custom_rule
#         else:
#             self.custom_rule = self.get_custom_rule()
#             return self.custom_rule

#     def get_custom_rule(self):
#         '''获取规则（自定义）'''
#         return None

#     def get_record_by_id(self, id):
#         '''
#         通过ID获取考勤记录

#         Parameters
#         ----------
#         id : int
#             考勤记录在数据库中的id

#         Returns
#         -------
#         models.Record
#             考勤记录对象
#         '''
#         return Record.objects.get(id=id)

#     def get_record_by_id_task(self, id, task):
#         '''
#         通过ID获取考勤记录

#         Parameters
#         ----------
#         id : int
#             考勤记录在数据库中的id
#         task : models.Task
#             考勤任务实例

#         Returns
#         -------
#         models.Record
#             考勤记录对象
#         '''
#         return Record.objects.get(task=task, id=id)

#     def undo_record(self, record, username,name):
#         '''
#         单个 核销考勤记录
#         通过给manager属性来表示已经核销
#         这个属性记录了是谁核销
#         核销判断逻辑就是根据是否存在这个属性

#         Parameters
#         ----------
#         record : models.Record
#             任务记录实例
#         manager_user : models.User
#             用户模型实例,Record表中manager字段
#         '''
#         record.manager_username = username
#         record.manager_name = name
#         record.save()

#     def submit_record(self, record_model):
#         '''
#         单个 提交考勤记录

#         '''
#         Record.objects.create(**record_model)


# class SubmitBase(TaskBase, RecordBase):
#     def get_room(self):
#         '''
#         获取房间,并且更新房间状态
#         '''
#         try:
#             room_id = str(self.request.params.room_id)
#             self.room_str = room_id
#             # 保存房间状态为已检查
#             dorm = DormCallCache()
#             dorm.set_room_status(room_id,self.task.types)
#             return room_id
#         except:
#             self.room_str = None
#             return None

#     def submit_check(self):
#         '''
#         提交前数据检查
#         在这里可以对考勤记录数据做最后的修改
#         执行完后就进入任务提交
#         只有返回False时不会提交
#         '''
#         pass

#     def submit_undo_record(self, record_model, manager_user):
#         '''
#         单个 核销考勤记录

#         Parameters
#         ----------
#         record_model : models.Record
#             任务记录实例
#         manager_user : models.User
#             用户模型实例
#         '''
#         self.undo_record(record_model, manager_user)

#     def get_context(self, request, *args, **kwargs):
#         # TODO 优化提交数度
#         self.get_task_player_by_user()
#         self.is_open()
#         self.custom_rule = None
#         self.get_room()
#         records = request.params.records

#         for record in records:
#             # 获取用户
#             user = {"username":'','name':''}
#             if 'user_id' in record.keys():
#                 user, flg = self.qrpc(
#                     'GetUserManage',
#                     {"username": record['user_id'], "type": "get_by_username"},
#                 )
#                 if not flg:
#                     return JsonResponse(user)
#             # 构建 考勤记录模型
#             record_model = {}
#             record_model['task'] = self.task
#             record_model['room_str'] = self.room_str
#             try:
#                 grade_str, flg = self.qrpc(
#                     'GradeManage',
#                     {"username": record['user_id'], "type": "get_grade_of_user"},
#                 )
#                 record_model['grade_str'] = grade_str
#             except:
#                 record_model['grade_str'] = None
#             record_model['student_approved_username'] = user['username']
#             record_model['student_approved_name'] = user['name']
#             record_model['worker_username'] = self.request.user.username
#             record_model['worker_name'] = self.request.user.name

#             status = str(record['status'])
#             # 撤销记录
#             if status == '1':
#                 record_model['manager'] = self.request.user
#                 self.submit_undo_record(record_model, user)

#             # 提交记录
#             elif status == '0':
#                 reason = record['reason']  # 自定义规则文本 / 规则ID
#                 reason_is_custom = record['reason_is_custom']

#                 rule_str = ''  # 规则文本
#                 rule = None  # 规则对象

#                 if reason_is_custom:  # 判断是否为自定义规则
#                     rule = self.init_custom_rule()
#                     rule_str = reason
#                 else:
#                     try:
#                         rule = RuleDetails.objects.get(id=reason)
#                         rule_str = rule.name
#                     except:
#                         rule = self.init_custom_rule()
#                         rule_str = reason

#                 record_model['rule_str'] = rule_str
#                 record_model['score'] = 1  # 默认扣一分
                
#                 if rule:
#                     record_model['rule'] = rule
#                     record_model['score'] = rule.score

#                 if self.submit_check(record_model, record) != False:
#                     self.submit_record(record_model)

#     class Meta:
#         records = {}
#         records['user_id'] = '用户ID'
#         records['reason'] = '规则内容'
#         records['status'] = '提交类型'
#         records['score'] = '自定义扣分'
#         records['reason_is_custom'] = '是否是自定义规则'

#         param_fields = (
#             ('records', fields.ListField(label=_('提交记录 '), default=records)),
#         )
#         path = '/'


# class DormCallCache(InitCacheConnection):
#     '''
#     寝室点名缓存
#     数据结构
#     KnowingRoom 3#101 0
#     HealthRoom  3#101 0
#     HealthUser  19510101 0
#     HealthUser  19510102 0
#     '''

#     KNOWING = 'Knowing'
#     HEALTH = 'Health'
#     ROOM = 'Room'
#     USER = 'User'
#     K_CALL = KNOWING + ROOM
#     H_CALL = HEALTH + ROOM
#     K_USER = KNOWING + USER
#     H_USER = HEALTH + USER
#     STUDENTS = 'Students'
#     def get_room_stu(self, room):
#         '''
#         获取房间里面的学生信息
#         Args:
#             room (str): 房间编号

#         Returns:
#             学生数据: {
#                         "房间号(3#104)":{
#                             "19510144":{
#                                 "username":xxx,
#                                 "name":xxx,
#                                 "bed_position":1,
#                                 "room":3#104,
#                             }
#                         }
#                     }
#         '''
#         d = self.cache.hget(DormCallCache.STUDENTS, room)
#         if not d:
#             return {}
#         return json.loads(d)
        
#     def get_stu_status(self,types,username):
#         '''
#         获取学生不同任务的考勤的状态

#         Args:
#             username (学号): 19510144
#             types (任务类型): 0 / 1 / 2

#         Returns:
#             int: 0/1 
#         '''
#         types = DormCallCache.get_type_by_dorm_key(types)
#         status = self.cache.hget(types+DormCallCache.USER, username)
#         if not status:
#             return 0
#         return status

#     def set_stu_status(self,room,types,username,status):
#         '''
#         设置学生不同任务的考勤的状态

#         Args:
#             room (寝室编号): 3#101
#             username (学号): 19510144
#             types (任务类型): 0 / 1 / 2

#         Returns:
#             int: 0/1 
#         '''
#         types = DormCallCache.get_type_by_dorm_key(types)
#         self.cache.hset(types+DormCallCache.USER, username,status)

#     def get_type_by_dorm_key(ty):
#         kv = {"0":DormCallCache.KNOWING,"1":DormCallCache.HEALTH}
#         return kv[ty]

#     def set_room_status(self,room_id,types):
#         '''
#         设置房间状态为已检查

#         Args:
#             room_id ([str]): 房间编号
#             types ([str]): 任务类型
#         '''
#         key = DormCallCache.get_type_by_dorm_key(types)
#         self.cache.hset(key + DormCallCache.ROOM,room_id,1)

#     # def set_dorm_building_health(self,floor,room):
#     #     floor_data = self.get_dorm_building_health(floor)
#     #     floor_data[room] = 1
#     #     self.hset(DormCallCache.KEY_B+DormCallCache.HEALTH,floor,floor_data)

#     def get_room_status(self,room,types):
#         '''
#         获取一个房间的考勤状态

#         Args:
#             room ([type]): [description]
#             types ([type]): [description]

#         Returns:
#             [type]: [description]
#         '''
#         key = DormCallCache.get_type_by_dorm_key(types)
#         return self.cache.hget(key + DormCallCache.ROOM,room)
    
#     # def get_floor_info(self,floor,types):
#     #     '''
#     #     获取 楼 层 考勤进度

#     #     Args:
#     #         floor ([type]): [description]
#     #         types ([type]): [description]

#     #     Returns:
#     #         int,int: 房间数量，已经检查的数量
#     #     '''
#     #     keys = self.cache.keys(DormCallCache.DORM + floor+'*')
#     #     # 已经检查的数量
#     #     compile = 0
#     #     k = self.get_type_by_dorm_key(types)
#     #     for key in keys:
#     #         n = int(self.cache.hget(key,k))
#     #         compile+=n
#     #     return len(keys),compile

#     def init_data(self):
#         # 检查是否存在缓存
#         k = self.cache.keys("*"+DormCallCache.ROOM)
#         if len(k)==2:
#             return self
        
#         # 考勤状态
#         knowing_room = {}
#         knowing_user = {}
#         health_room = {}
#         health_user = {}

#         # 入住信息
#         accommodations = {}

#         username_info_list = []

#         # 获取寝室学生入住信息
#         rsp, flg = self.qrpc('BuildingManagr', {"type": "filter_stu_room_all"})
#         if not flg:
#             return self
        
#         for d in rsp:
#             username = d['username']
#             room = d['room']

#             # 查寝状态
#             knowing_room[room] = 0
#             knowing_user[username] = 0
#             # 查卫生状态
#             health_room[room] = 0
#             health_user[username] = 0

#             # 初始化住宿数据
#             try:
#                 accommodations[room][username]=d
#             except:
#                 if room not in accommodations.keys():
#                     accommodations[room] = {}
#                     accommodations[room][username]=d
#             username_info_list.append(d['username'])

#         # 请求用户基本信息
#         rsp, flg = self.qrpc('GetUserManage', {"username_list":username_info_list, "type": "fileter_user_by_username"})
#         if not flg:
#             return self
            
#         username_name_dict = {}
#         for u in rsp:
#             # 拼接学号-姓名字典
#             username_name_dict[u['username']] = u['name']

#         # 保存寝室包含的学生信息
#         for room in accommodations:
#             stu = accommodations[room]
#             for u in stu:
#                 stu[u]['id'] = u
#                 try:
#                     stu[u]['name'] = username_name_dict[u]
#                 except:
#                     stu[u]['name'] = u
                    
#             accommodations[room] = json.dumps(stu)
#         self.cache.hmset(DormCallCache.STUDENTS, accommodations)
#         self.cache.hmset(DormCallCache.K_CALL, knowing_room)
#         self.cache.hmset(DormCallCache.K_USER, knowing_user)
#         self.cache.hmset(DormCallCache.H_CALL, health_room)
#         self.cache.hmset(DormCallCache.H_USER, health_user)
#         return self


# class UserCallCache( InitCacheConnection):
#     '''
#     用户点名缓存
#     缓存数据结构
#     "UserCall", {
#             "班级": {
#                "username":{
#                 "user_id":'12'
#                     "username": '19',
#                     "name": '姓名',
#                     "rule_1": 0,
#                     "rule_2": 0,
#                 }
#             }
#     }
#     Args:
#         RpcCoolBFFAPIView ([type]): [description]
#     '''

#     # TODE 数据结构出现userid重复 需要和前端一起修改

#     KEY_SPACE = 'UserCall'

#     def clear(self):
#         self.init_all_grades_call()

#     def get_grade_call(self, class_id):
#         '''从缓存获取班级点名名单'''
#         flg = self.cache.hexists(UserCallCache.KEY_SPACE, class_id)
#         if not flg:
#             self.update_grades_call_cache([class_id])
#         json_str = self.cache.hget(UserCallCache.KEY_SPACE, class_id)
#         return json.loads(json_str)

#     def init_all_grades_call(self, task=None):
#         '''
#         更新晚自修点名任务所有班级内学生信息
#         '''
#         if not task:
#             # 获取所有晚自修任务的班级列表
#             task = Task.objects.filter(types='2')

#         grades = []
#         for t in task:
#             grade = t.get_grades()
#             grades = grades + grade
#         self.update_grades_call_cache(grades)

#     def update_grades_call_cache(self, grades):
#         '''
#         更新多个班级的点名数据

#         Args:
#             grades ([type]): [description]
#         '''

#         grades_dict = {}
#         for g in grades:
#             grades_dict[g] = []

#         # 获取班级对应的所有学生学号
#         rsp, flg = self.qrpc(
#             'GradeManage',
#             {"grade_name_list": grades, "type": "get_users_by_grade_names"},
#         )
#         username_list = []
#         for user in rsp:
#             username_list.append(user['username'])
#             grades_dict[user['grade']].append(user['username'])

#         # 获取所有学号对应的学生信息
#         rsp, flg = self.qrpc(
#             'GetUserManage',
#             {'username_list': username_list, 'type': 'fileter_user_by_username'},
#         )

#         # 整理学生个人信息
#         user_dict_by_username = {}
#         for u in rsp:
#             user_info = {}
#             user_info['username'] = u['username']
#             user_info['user_id'] = u['username']
#             user_info['name'] = u['name']
#             user_dict_by_username[u['username']] = user_info

#         # 拼接 班级->学生信息
#         cache_user_call = {}
#         for g in grades:
#             grade_dict = {}
#             for username in grades_dict[g]:
#                 try:
#                     grade_dict[username] = user_dict_by_username[username]
#                 except:
#                     grade_dict[username] = {
#                         "username": username,
#                         "user_id": username,
#                         "name": '空',
#                     }
#             cache_user_call[g] = json.dumps(grade_dict)

#         # 更新
#         self.cache.hmset(UserCallCache.KEY_SPACE, cache_user_call)


# class ExcelInData(PermissionView, ExcelBase):
#     '''
#     获取和学生有关的Excel表格
#     '''

#     def init(self, request):
#         '''
#         初始化数据


#         Args:
#             request ([type]): [description]
#         '''
#         self.db_users = {}
#         self.message_list = []
#         self.rows = self.excel_to_list(request)
#         self.init_excel_user()

#     def init_excel_user(self):
#         # 获取涉及的学生对象列表

#         user_usernams = []
#         for row in self.rows:
#             username = row['username']
#             user_usernams.append(username)

#         # query, flg = self.qrpc(
#         #     'GetUserManage',
#         #     {'username_list': user_usernams, 'type': 'fileter_user_by_username'},
#         # )
#         conn = InitCacheConnection()
#         query = conn.cache.hmget('User',user_usernams)
#         for u in query:
#             if u:
#                 u = json.loads(u)
#                 self.db_users[u['username'].upper()] = u

#         rows_ = []
#         for row in self.rows:
#             username = row['username']
#             name = row['name']
#             # TODO 检查是否包含关键数据
#             try:
#                 u = self.db_users[username]
#             except:
#                 self.add_message(username, self.get_name(username), '用户不在系统')
#                 continue

#             if name != None and name != u['name']:
#                 self.add_message(username, name, '学号与姓名不一致 系统内部为:' + u.name)
#                 continue

#             try:
#                 u['grade']
#             except:
#                 self.add_message(username, self.get_name(username), '用户没有班级信息异常')
#                 continue

#             row['username'] = row['username'].upper()
#             rows_.append(row)
#         self.rows = rows_

#     def add_message(self, *d):
#         '''
#         添加需要返回前端的信息
#         '''
#         self.message_list.append(d)

#     def get_name(self, name):
#         # 获取用户实例
#         try:
#             return self.db_users[name].name
#         except:
#             return name

#     def time_formatting(self, time):
#         # 表格时间格式化为 2000/1/1
#         if '-' in time:
#             time = time.split(' ')[0]
#             time = time.replace('-', '/')

#         year = time.split('/')[0]
#         month = int(time.split('/')[1])
#         data = int(time.split('/')[2])
#         time = year + '/' + str(month) + '/' + str(data)
#         return time

#     def time_format_one(self, time):
#         '''
#         字符串转datetime对象

#         Args:
#             time (str): '2021-10-01 13:59:59.999'

#         Returns:
#             [type]: [description]
#         '''
#         time = time.split('.')[0].strip()
#         time = time.replace('/', '-')
#         f = '%Y-%m-%d %H:%M:%S'
#         t = datetime.datetime.strptime(time, f)
#         if t.minute == 59 and t.second == 59:
#             t += datetime.timedelta(seconds=1)
#         return t

#     class Meta:
#         path = '/'


# class MultipleRecordQueryCriteria:

#     def query_data(self,request):
#         username = request.params.username
#         college_id = request.params.college_id
#         start_date = get_start_date(request)
#         end_date = get_end_date(request)
#         q4 = Q(task__types__in=['2', '0', '3']) #| Q(rule_str='早签')  # 任务类型限制
#         q5 = Q(task__college=college_id)  # 分院
#         q6 = Q(rule__isnull=False)
#         if username:
#             q_user = Q(student_approved_username=username) | Q(student_approved_name=username)
#         else:
#             q_user = Q()

#         records = Record.objects.filter(
#             q4,q5,q6,q_user,
#             star_time__range=(start_date, end_date),
#             manager_username__isnull=True,
#         )
#         return records
