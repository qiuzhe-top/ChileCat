"""管理视图"""
import logging

from Apps.SchoolAttendance import models as SchoolAttendanceModels
from Apps.SchoolInformation.models import StuInRoom
from Apps.User.models import College, Grade
from cool import views
from cool.views import (CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite,
                        sites)
from cool.views.view import CoolBFFAPIView
from core.excel_utils import excel_to_list
from core.models_utils import search_room
from core.permission_group import user_group
from core.settings import *
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from django.utils.translation import gettext_lazy as _
from openpyxl import load_workbook
from openpyxl.reader.excel import ExcelReader
from rest_framework.views import APIView

User = get_user_model()
logger = logging.getLogger(__name__)


site = ViewSite(name='SchoolInformation', app_name='SchoolInformation')


def create_class(class_name, college_name):
    """创建班级"""
    if not Grade.objects.filter(name=class_name).exists():
        if not College.objects.filter(name=college_name).exists():
            college = College(name=college_name)
            college.save()
            print("分院:", college, "创建.")
        college = College.objects.get(name=college_name)
        grade = Grade(name=class_name, college=college)
        grade.save()
        print("班级", grade, "创建")
        return grade
    print("班级已存在,无需创建!")
    return None


# excel 转 列表 当第一个单元格为空是过滤这行数据

# 用户与组的管理
def group_user(request):
    '''用户与组的管理'''
    ret = {}
    list_ = excel_to_list(request)
    for row in list_:
        group = row[0]
        username = row[1]
        flg = row[2]
        # 当 组为'-'学号有参 时 清空用户所在的所有组
        if group == '-' and username != None:

            pass
        # 当 学号为'-'组有参 时 清空组内的用户
        elif username == '-' and group != None:
            error = user_group.group_clean(group)
        # 根据flg的状态执行删除/添加
        elif group != None and username != None and flg != None:
            if flg == '+':
                # 组里面添加学生
                error = user_group.group_add_user(
                    group,
                    [
                        username,
                    ],
                )
            elif flg == '-':
                # pass
                error = user_group.group_remove_user(
                    group,
                    [
                        username,
                    ],
                )
                # 组里面删除学生
    ret['error'] = error
    return ret


# 导入学生
def user_init(request):
    '''导入学生'''
    excel = excel_to_list(request)
    excel_users = {}
    excel_grades = {}
    for row in excel:
        grade = row[0]
        username = row[1]
        name = row[2]
        excel_users[username] = {
            "username":username,
            "grade":grade,
            "name":name,
        }
        excel_grades[grade] = ''


    # 创建DB没有的班级
    db_grades = dict(Grade.objects.all().values_list('name','id'))
    grades =  excel_grades.keys() - db_grades.keys()
    wait_create_grades=[]
    for grade in grades:
        wait_create_grades.append(Grade(name=grade))
    Grade.objects.bulk_create(wait_create_grades)
    # 通过excel里面的班级集合获取班级实例列表
    db_grades = Grade.objects.filter(name__in=excel_grades.keys())
    for grade in db_grades:
        name = grade.name
        excel_grades[name] = grade # 完善从excel里面获取的班级列表 改为班级实例

    db_users =dict(User.objects.all().values_list('username','name')) # 这里取name只为完成dict
    username_list =  excel_users.keys() - db_users.keys() # 取出DB不存在的用户
    wait_create_users=[]
    for username in username_list:
        # 构建用户实例
        grade_str = excel_users[username]['grade']
        grade_obj = excel_grades[grade_str]
        excel_users[username]['grade'] = grade_obj
        excel_users[username]['password'] = PASSWOED_123456
        user = User(**excel_users[username])
        wait_create_users.append(user)
    User.objects.bulk_create(wait_create_users)
    return {'create_user':username_list}


# 用户组初始化
def group_init(request=None):
    '''用户组初始化'''
    print('用户组初始化')
    names = [
        # 考勤任务管理 # 后台导航栏是否展示 <考勤系统> 父选项
        'task_admin',
        # 考勤数据管理
        'task_data',
        # 检查卫生
        'health_admin',
        # 晚自修
        'late_admin',
        # 晚查寝
        'knowing_admin',
    ]
    d = user_group.group_init(names)
    ret = {"message": d, "names": names}
    return ret


# 用户寝室关联
def user_room(request):
    '''用户寝室关联'''
    rows = excel_to_list(request)
    message = {}
    message['username-'] = []
    message['flg-'] = []
    message['flg+'] = []
    message['update'] = []
    message['error'] = []
    for row in rows:
        try:
            room_ = row[0]
            username_ = row[1]
            flg = row[2]

            # 清空寝室内的学生
            if username_ == "-":
                room = search_room(room_)
                room.stu_in_room.all().delete()
                message['username-'].append(room_ + "：清空")

            elif flg == '-':
                user = User.objects.get(username=username_)
                StuInRoom.objects.filter(user=user).delete()
                message['flg-'].append(room_ + " 删除 " + username_)
                
            # 学生寝室绑定/删除
            elif flg == '+':
                user = User.objects.get(username=username_)
                room = search_room(room_)
                st, flg = StuInRoom.objects.get_or_create(
                    user=user, defaults={"room": room}
                )
                st.room = room
                st.save()
                if flg:
                    message['flg+'].append(room_ + " 添加 " + username_)
                else:
                    message['update'].append(username_ + " 更新为 " + room_)

            
        except Exception as e:
            message['error'].append(username_)

    return message


def init_Attendance_group(request=None):
    '''考勤权限分组'''
    print('考勤权限分组')
    # task_data 组
    name3 = 'task_data'
    per3 = [
        'undo_record_admin',
        'zq_data_import',
    ]
    user_group.group_add_permission(name3, per3)
    return 2000


def add_user():
    L = [
        ['195401', '19540140'],
        ['195303', '19530338'],
        ['195303', '19530345'],
    ]


# 晚自修规则
def uinitialization_rules(request=None):
    '''考勤规则初始化
    codename:系统内部使用不能随意修改 导出Excel会使用
    '''
    print('晚自修规则初始化')
    # TODO 效率低
    res = []
    for item in INIT_RULES:
        rule_f = item['rule_f']
        rules = item['rules']
        rule, flg = SchoolAttendanceModels.Rule.objects.get_or_create(**rule_f)
        if flg:
            res.append(rule_f['name'])
        for r in rules:
            r['rule'] = rule
            SchoolAttendanceModels.RuleDetails.objects.get_or_create(**r)
    return res


def run_init(request):

    return {
        "group_init": group_init(request),
        "uinitialization_rules": uinitialization_rules(request),
        "init_Attendance_group": init_Attendance_group(request),
    }


@site
class DataInit(CoolBFFAPIView):
    name = "系统数据初始化"

    def get_context(self, request):
        init_dict = {
            "init": run_init,
            # 导入学生
            "user_init": user_init,
            # 用户寝室关联
            "user_room": user_room,
            # 用户与组的管理
            "group_user": group_user,
        }
        type_ = request.data['type']
        data = init_dict[type_](request)
        return data

from django.shortcuts import render


@site
class Index(CoolBFFAPIView):
    name = _('后台主页')
   
    def get_context(self, request, *args, **kwargs):
        data = []
        u = User.objects.all().count()
        t = SchoolAttendanceModels.Record.objects.all().count()
        context = { 'user_count': u, 'task_count': t }
        return render(request, 'index/index.html',context)

from cool.views.utils import get_api_info, get_url, get_view_list


@site
class Getapis(CoolBFFAPIView):
    name = 'api接口'
    method = 'GET'
    tag = {
        "/api/school_information": "学校信息",
        "/api/school_attendance": "考勤管理",
        "/api/manage": "系统管理",
        "/api/user": "用户管理",
    }
    # 地址
    def get_url(self):
        # "/school/attendance/task/switch"
        url = self.info['url'][4:]
        return url

    # Body请求参数
    def get_urlencoded(self):
        d = {}
        required = []
        if self.get_method() != 'post':
            return d, required
        params = self.info['info']['request_info']
        for param in params:
            d[param] = {
                "type": params[param]['type'],
                "description": params[param]['label'],
                "example": params[param]['default_format'],
            }
            f = params[param]['required'] == True
            if f:
                required.append(param)
        return d, required

    # Get请求参数
    def get_parameters(self):
        data = []
        data.append(
            {
                "name": "token",
                "in": "header",
                "description": "",
                "required": False,
                "example": "",
                "schema": {"type": "string"},
            }
        )
        if self.get_method() != 'get':
            return data
        params = self.info['info']['request_info']

        for param in params:
            data.append(
                {
                    "name": param,
                    "in": "query",
                    "description": params[param]['label'],
                    "required": params[param]['required'],
                    "example": params[param]['default_format'],
                    "schema": {"type": params[param]['type']},
                }
            )
        return data

    # 返回参数
    def get_response_info(self):
        # response_info_format
        response_info = self.info['info']['response_info']
        data = response_info.get('data', [])
        response_data = {}
        if data:
            for k in data:
                response_data[k] = {
                    "type": "string",
                    "description": data[k]
                }

        d = {
            "code": {
                "type": "integer",
                "minimum": 0,
                "maximum": 0,
                "description": "状态码",
            },
            "message": {"type": "string", "description": "提示信息"},
            "data": {
                "type": "object",
                "properties": response_data,
                "description": "数据",
            },
        }
        return d, response_info

    # 当前接口分组
    def tags(self):
        self.tag
        url = str(self.info['url'])
        index = url.find('/', url.find('/', 1) + 1)
        key = url[:index]
        return [self.tag[key]]

    def tag_header(self):
        v = self.tag.values()
        d = []
        for i in v:
            d.append({'name': i})
        return d

    def get_method(self):
        return str.lower(getattr(self.view_class, "method", "post"))

    def get_context(self, request, *args, **kwargs):
        views = get_view_list()
        items = []
        apis = {}
        apis['openapi'] = '3.0.1'
        apis["info"] = {"title": "示例项目", "description": "", "version": "1.0.0"}
        apis['name'] = 'Django 导出'
        apis['tags'] = self.tag_header()
        apis['paths'] = {}
        for v in views:
            self.view_class = v['view_class']

            api_info = get_api_info(self.view_class)
            self.info = api_info['apis'][0]
            url = self.get_url()
            tags = self.tags()
            req, required = self.get_urlencoded()
            parameters = self.get_parameters()
            method = self.get_method()
            rep, response_info = self.get_response_info()

            name = self.info['name']

            apis['paths'][url] = {
                method: {
                    "summary": name,
                    "description": "",
                    "tags": tags,
                    "parameters": parameters,
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {
                                    "type": "object",
                                    "properties": req,
                                    "required": required,
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "成功",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": rep,
                                        "required": [],
                                    },
                                    # "examples": {
                                    #     "1": {"summary": "成功示例", "value": response_info}
                                    # },
                                }
                            },
                        }
                    },
                }
            }
            # apis['item'].append(api)
        return JsonResponse(apis)


from django.http import HttpResponse


@site
class Apitouviews(CoolBFFAPIView):
    name = _('api转uViewsApi模板')

    def get_method(self):
        return str.lower(getattr(self.view_class, "method", "post"))

    def get_url(self):
        url = self.info['url']
        return url

    def get_context(self, request, *args, **kwargs):
        views = get_view_list()
        api_str = ""
        for v in views:
            self.view_class = v['view_class']
            api_info = get_api_info(self.view_class)
            self.info = api_info['apis'][0]
            url = self.get_url()
            name = self.info['name']
            method = self.get_method()
            ul_name = self.info['ul_name'][4:]
            t1 = "// {} \n"
            t2 = "api['{}'] = (params = {}) => vm.$u.{}('{}', params) \n"
            t = (t1 + t2).format(name,ul_name,'{ }',method,url)
            api_str += t
        return HttpResponse(api_str)
# 可以慢慢淘汰的代码

# def put_stu_room(stu, room, ret):
#     """把学生放入寝室,注意第二个参数目前只支持xx#xxx形式"""
#     history = StuInRoom.objects.filter(room=search_room(room), user=stu)
#     try:
#         if history.exists():
#             ret.append(
#                 "学生" + stu.userinfo.name + "->" + history.first().get_room() + "已存在"
#             )
#         else:
#             room = search_room(room)
#             stu_in_room = StuInRoom.objects.get_or_create(room=room, user=stu)
#             ret.append(
#                 "记录("
#                 + "学号:"
#                 + stu.username
#                 + "姓名:"
#                 + stu.userinfo.name
#                 + "->"
#                 + stu_in_room[0].get_room()
#                 + "寝室)已创建"
#             )
#     except:
#         ret.append(str(stu) + "异常")


# def import_stu_data(request):
#     """寝室表导入"""
#     file = request.data['file']
#     work_book = load_workbook(file)
#     ret = []
#     for sheet in work_book:
#         room_name = ""
#         for info in sheet.values:
#             if info[0] == "寝室日".strip():
#                 continue
#             try:
#                 if info[0]:
#                     room_name = str(info[0])[0 : info[0].find("#") + 3 + 1]
#                 name = ''.join(re.findall('[\u4e00-\u9fa5]', str(info[2]))).strip()
#                 if len(name) == 0 or not name:
#                     continue
#                 grade = str(info[3]).strip()
#                 stu_id = str(info[4]).strip()
#                 tel = str(info[5]).strip()
#                 user = User.objects.get_or_create(username=stu_id)
#                 user_info, flg0 = UserInfo.objects.get_or_create(user=user[0])
#                 user_info.name = name
#                 user_info.tel = tel
#                 user_info.save()

#                 grade = Grade.objects.get_or_create(name=grade)
#                 stu_info, flg1 = StudentInfo.objects.get_or_create(
#                     user=user[0], defaults={"grade": grade[0]}
#                 )
#                 if not flg1:
#                     stu_info.grade = grade[0]
#                     stu_info.save()
#                 put_stu_room(user[0], room_name, ret)
#             except User.DoesNotExist:
#                 ret.append(info[2] + name + "异常")
#             except UserInfo.DoesNotExist:
#                 ret.append(info[2] + name + "异常")
#             except:
#                 ret.append(info[2] + "---获取数据异常")

#     return ret

# # 导入学生
# def user_init(request):
#     '''导入学生'''
#     message_list = {}
#     message_list['create'] = []
#     message_list['update'] = []
#     excel = excel_to_list(request)
#     grade_list = list()
#     user_list = list()
#     user_info_list = list()
#     stu_info_list = list()
#     for row in excel:
#         grade = row[0]
#         username = row[1]
#         name = row[2]
#         # 创建/获取 班级
#         grade = Grade(name=grade)
#         grade_list.append(grade)
#         # 创建/获取 用户对象
#         user = User(username=username)
#         user.set_password(username)
#         user_list.append(user)
#         user_info = UserInfo(user=user, name=name)
#         stu_info = StudentInfo (user=user, grade=grade)
#         user_info_list.append(user_info)
#         stu_info_list.append(stu_info)
#     Grade.objects.bulk_create(grade_list)
#     User.objects.bulk_create(user_info_list)
#     UserInfo.objects.bulk_create(user_info_list)
#     StudentInfo.objects.bulk_create(stu_info_list)
#     return message_list
# class In_zaoqian_excel(APIView):
#     def post(self, request):
#         """针对寝室表"""
#         file = request.data['file']

#         file_name = str(time.time()) + '__' + file.name
#         file_path = os.path.join('upload', file_name)
#         f = open(file_path, 'wb')
#         for i in file.chunks():  # chunks方法是一点点获取上传的文件内容
#             f.write(i)
#         f.close()

#         file_name = 'upload//' + file_name

#         # return JsonResponse({})

#         wb = load_workbook(file, read_only=True)

#         error_list = []
#         for rows in wb:
#             for row in rows:  # 遍历行
#                 username = row[0].internal_value
#                 name = row[1].internal_value
#                 str_time = row[3].internal_value
#                 is_header = (
#                     username.find('考勤') != -1
#                     or username.find('统计') != -1
#                     or username.find('员工号') != -1
#                 )
#                 if (
#                     not (username == None or name == None or str_time == None)
#                     and not is_header
#                 ):
#                     print(username)
#                     try:
#                         u = User.objects.get(username=username)
#                         try:
#                             str_time = datetime.datetime.strptime(str_time, '%Y/%m/%d')
#                             d = {
#                                 'rule_str': '旷早签',
#                                 'student_approved': u,
#                                 'score': 1,
#                                 'star_time': str_time,
#                             }
#                             (
#                                 sa,
#                                 flg,
#                             ) = SchoolAttendanceModels.Record.objects.get_or_create(**d)
#                             sa.worker = request.user
#                             sa.save()
#                         except:
#                             error_list.append(
#                                 {
#                                     'username': username,
#                                     'name': name,
#                                     'str_time': str_time,
#                                     'message': '导入记录失败',
#                                 }
#                             )
#                     except:
#                         error_list.append(
#                             {
#                                 'username': username,
#                                 'name': name,
#                                 'str_time': str_time,
#                                 'message': '用户不存在',
#                             }
#                         )

#         ret = {'message': '添加成功 请检查添加结果', 'code': '2000', 'data': error_list}
#         return JsonResponse(ret)


urls = site.urls
urlpatterns = site.urlpatterns
