'''
Author: 邹洋
Date: 2022-02-08 11:49:52
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-08 12:20:00
Description: 
'''
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from AppInformation.models import StuInRoom
from rest_framework import fields

from core.common.excel import ExcelBase
from django.utils.translation import gettext_lazy as _

site = ViewSite(name='OS', app_name='OS')

# # 导入学生
# def user_init(request):
#     '''导入学生'''
#     excel = ExcelBase().excel_to_list(request)
#     excel_users = {}
#     excel_grades = {}
#     # 获取分院实例
#     try:
#         college = College.objects.get(code_name=request.data['college_codename'])
#     except:
#         raise CoolAPIException(ErrorCode.NO_COLLEGE_CODE)

#     for row in excel:
#         row_len = len(row)
#         grade = row['grade']
#         username = row['username']
#         name = row['name']
#         tel =  row['tel'] if row_len > 3 and row['tel'] else None
#         excel_users[username] = {
#             "username": username,
#             "grade": grade,
#             "name": name,
#             "tel": tel,
#         }
#         # if tel:
#         #     create_other_data(row)
#         excel_grades[grade] = ''

#     # 创建DB没有的班级
#     db_grades = dict(Grade.objects.all().values_list('name', 'id'))
#     grades = excel_grades.keys() - db_grades.keys()
#     wait_create_grades = []
#     for grade in grades:
#         wait_create_grades.append(Grade(name=grade, college=college))
#     Grade.objects.bulk_create(wait_create_grades)

#     # 通过excel里面的班级集合获取班级实例列表
#     db_grades = Grade.objects.filter(name__in=excel_grades.keys())
#     for grade in db_grades:
#         name = grade.name
#         excel_grades[name] = grade  # 完善从excel里面获取的班级列表 改为班级实例

#     db_users = dict(
#         User.objects.all().values_list('username', 'name')
#     )  # 这里取name只为完成dict
#     username_list = excel_users.keys() - db_users.keys()  # 取出DB不存在的用户
#     wait_create_users = []
#     for username in username_list:
#         # 构建用户实例
#         grade_str = excel_users[username]['grade']
#         grade_obj = excel_grades[grade_str]
#         excel_users[username]['grade'] = grade_obj
#         excel_users[username]['password'] = PASSWOED_123456
#         user = User(**excel_users[username])
#         wait_create_users.append(user)
#     User.objects.bulk_create(wait_create_users)
#     return {'create_user': username_list}

# # 测试维护时用来处理导入其它用户 信息
# def create_other_data(row):
#     row_len = len(row)
#     username = row[1]
#     tel =  row[3] if row_len > 3 else None
#     User.objects.filter(username=username).update(tel=tel)



# # 用户组初始化
# def group_init(request=None):
#     '''用户组初始化'''
#     print('用户组初始化')
#     names = [
#         # 考勤任务管理 # 后台导航栏是否展示 <考勤系统> 父选项
#         'task_admin',
#         # 考勤数据管理
#         'task_data',
#         # 检查卫生
#         'health_admin',
#         # 晚自修
#         'late_admin',
#         # 晚查寝
#         'knowing_admin',
#     ]
#     d = group.group_init(names)
#     ret = {"message": d, "names": names}
#     return ret


# # 用户寝室关联
# def user_room(request):
#     '''用户寝室关联'''
#     rows = ExcelBase().excel_to_list(request)
#     message = {}
#     message['username-'] = []
#     message['type-'] = []
#     message['type+'] = []
#     message['update'] = []
#     message['error'] = []
#     for row in rows:
#         try:
#             room_ = row['room']
#             username_ = row['username']
#             type = row['type']

#             # 清空寝室内的学生
#             if username_ == "-":
#                 room = search_room(room_)
#                 room.stu_in_room.all().delete()
#                 message['username-'].append(room_ + "：清空")
#             # 删除学生对应的寝室
#             elif type == '-':
#                 user = User.objects.get(username=username_)
#                 StuInRoom.objects.filter(user=user).delete()
#                 message['type-'].append('删除' +username_+'对应的寝室' )

#             # 学生寝室绑定/删除
#             elif type == '+':
#                 user = User.objects.get(username=username_)
#                 room = search_room(room_)
#                 st, type = StuInRoom.objects.get_or_create(
#                     user=user, defaults={"room": room}
#                 )
#                 st.room = room
#                 st.save()
#                 if type:
#                     message['type+'].append(room_ + " 添加 " + username_)
#                 else:
#                     message['update'].append(username_ + " 更新为 " + room_)

#         except Exception as e:
#             message['error'].append(username_)

#     return message


# def init_Attendance_group(request=None):
#     '''考勤权限分组'''
#     print('考勤权限分组')
#     # task_data 组
#     name3 = 'task_data'
#     per3 = [
#         'undo_record_admin',
#         'zq_data_import',
#     ]
#     group.group_add_permission(name3, per3)
#     return 2000


# def add_user():
#     L = [
#         ['195401', '19540140'],
#         ['195303', '19530338'],
#         ['195303', '19530345'],
#     ]


# # 晚自修规则
# def uinitialization_rules(request=None):
#     '''考勤规则初始化
#     codename:系统内部使用不能随意修改 导出Excel会使用
#     '''
#     print('晚自修规则初始化')
#     # TODO 效率低
#     res = []
#     for item in INIT_RULES:
#         rule_f = item['rule_f']
#         rules = item['rules']
        
#         rule, flg = SchoolAttendanceModels.Rule.objects.get_or_create(**rule_f) # 一级规则
#         if flg:
#             res.append('创建：' + rule_f['name'])
#         else:
#             res.append('存在：' + rule_f['name'])

#         for r in rules:
#             rule_detail = SchoolAttendanceModels.RuleDetails.objects.get_or_create(
#                 id=r['id'], name=r['name'], score=r['score'], rule=rule
#             )[0] # 二级规则
#             if 'child' in r.keys():
#                 for child_rule in r['child']:
#                     child_rule['rule'] = rule
#                     child_rule['parent_id'] = rule_detail
#                     SchoolAttendanceModels.RuleDetails.objects.get_or_create(**child_rule) # 三级规则
#     return res


# def init_college():
#     for c in COLLEGE_LIST:
#         College.objects.get_or_create(name=c['name'], code_name=c['codename'])
#     return COLLEGE_LIST


# def run_init(request):

#     return {
#         "group_init": group_init(request),
#         "uinitialization_rules": uinitialization_rules(request),
#         "init_Attendance_group": init_Attendance_group(request),
#         "init_college": init_college(),
#     }

# # 用户与组的管理
# def group_user(request):
#     '''用户与组的管理'''
#     ret = {}
#     list_ = ExcelBase().excel_to_list(request)
#     for row in list_:
#         group = row[0]
#         username = row[1]
#         flg = row[2]
#         # 当 组为'-'学号有参 时 清空用户所在的所有组
#         if group == '-' and username != None:

#             pass
#         # 当 学号为'-'组有参 时 清空组内的用户
#         elif username == '-' and group != None:
#             error = group.group_clean(group)
#         # 根据flg的状态执行删除/添加
#         elif group != None and username != None and flg != None:
#             if flg == '+':
#                 # 组里面添加学生
#                 error = group.group_add_user(
#                     group,
#                     [
#                         username,
#                     ],
#                 )
#             elif flg == '-':
#                 # pass
#                 error = group.group_remove_user(
#                     group,
#                     [
#                         username,
#                     ],
#                 )
#                 # 组里面删除学生
#     ret['error'] = error
#     return ret



@site
class DataInit(CoolBFFAPIView):
    name = "系统数据初始化"

    def get_context(self, request, *args, **kwargs):
        # init_dict = {
        #     "init": run_init,
        #     # 导入学生
        #     "user_init": user_init,
        #     # 用户寝室关联
        #     "user_room": user_room,
        #     # 用户与组的管理
        #     "group_user": group_user,
        # }
        # if request.method=='POST':
        #     type_ = request.data['type']
        #     data = init_dict[type_](request)
        # elif request.method=='GET':
        #     data = run_init(request)
        # return data
        pass


# @site
# class Getapis(CoolBFFAPIView):
#     name = 'api接口'
#     method = 'GET'
#     tag = {
#         "/api/school_information": "学校信息",
#         "/api/school_attendance": "考勤管理",
#         "/api/manage": "系统管理",
#         "/api/user": "用户管理",
#     }
#     # 地址
#     def get_url(self):
#         # "/school/attendance/task/switch"
#         url = self.info['url'][4:]
#         return url

#     # Body请求参数
#     def get_urlencoded(self):
#         d = {}
#         required = []
#         if self.get_method() != 'post':
#             return d, required
#         params = self.info['info']['request_info']
#         for param in params:
#             d[param] = {
#                 "type": params[param]['type'],
#                 "description": params[param]['label'],
#                 "example": params[param]['default_format'],
#             }
#             f = params[param]['required'] == True
#             if f:
#                 required.append(param)
#         return d, required

#     # Get请求参数
#     def get_parameters(self):
#         data = []
#         data.append(
#             {
#                 "name": "token",
#                 "in": "header",
#                 "description": "",
#                 "required": False,
#                 "example": "",
#                 "schema": {"type": "string"},
#             }
#         )
#         if self.get_method() != 'get':
#             return data
#         params = self.info['info']['request_info']

#         for param in params:
#             data.append(
#                 {
#                     "name": param,
#                     "in": "query",
#                     "description": params[param]['label'],
#                     "required": params[param]['required'],
#                     "example": params[param]['default_format'],
#                     "schema": {"type": params[param]['type']},
#                 }
#             )
#         return data

#     # 返回参数
#     def get_response_info(self):
#         # response_info_format
#         response_info = self.info['info']['response_info']
#         data = response_info.get('data', [])
#         response_data = {}
#         if data:
#             for k in data:
#                 response_data[k] = {"type": "string", "description": data[k]}

#         d = {
#             "code": {
#                 "type": "integer",
#                 "minimum": 0,
#                 "maximum": 0,
#                 "description": "状态码",
#             },
#             "message": {"type": "string", "description": "提示信息"},
#             "data": {
#                 "type": "object",
#                 "properties": response_data,
#                 "description": "数据",
#             },
#         }
#         return d, response_info

#     # 当前接口分组
#     def tags(self):
#         self.tag
#         url = str(self.info['url'])
#         index = url.find('/', url.find('/', 1) + 1)
#         key = url[:index]
#         return [self.tag[key]]

#     def tag_header(self):
#         v = self.tag.values()
#         d = []
#         for i in v:
#             d.append({'name': i})
#         return d

#     def get_method(self):
#         return str.lower(getattr(self.view_class, "method", "post"))

#     def get_context(self, request, *args, **kwargs):
#         views = get_view_list()
#         items = []
#         apis = {}
#         apis['openapi'] = '3.0.1'
#         apis["info"] = {"title": "示例项目", "description": "", "version": "1.0.0"}
#         apis['name'] = 'Django 导出'
#         apis['tags'] = self.tag_header()
#         apis['paths'] = {}
#         for v in views:
#             self.view_class = v['view_class']

#             api_info = get_api_info(self.view_class)
#             self.info = api_info['apis'][0]
#             url = self.get_url()
#             tags = self.tags()
#             req, required = self.get_urlencoded()
#             parameters = self.get_parameters()
#             method = self.get_method()
#             rep, response_info = self.get_response_info()

#             name = self.info['name']

#             apis['paths'][url] = {
#                 method: {
#                     "summary": name,
#                     "description": "",
#                     "tags": tags,
#                     "parameters": parameters,
#                     "requestBody": {
#                         "content": {
#                             "application/x-www-form-urlencoded": {
#                                 "schema": {
#                                     "type": "object",
#                                     "properties": req,
#                                     "required": required,
#                                 }
#                             }
#                         }
#                     },
#                     "responses": {
#                         "200": {
#                             "description": "成功",
#                             "content": {
#                                 "application/json": {
#                                     "schema": {
#                                         "type": "object",
#                                         "properties": rep,
#                                         "required": [],
#                                     },
#                                     # "examples": {
#                                     #     "1": {"summary": "成功示例", "value": response_info}
#                                     # },
#                                 }
#                             },
#                         }
#                     },
#                 }
#             }
#             # apis['item'].append(api)
#         return JsonResponse(apis)


admin_urls = site.urls
admin_urlpatterns = site.urlpatterns
