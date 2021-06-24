"""管理视图"""
from copy import error
import Manage
from Apps.SchoolInformation.models import *
import logging
import os
# import re
from django.http import JsonResponse, HttpResponse
from openpyxl import load_workbook
from rest_framework.views import APIView
from Apps.Permission.utils import expand_permission
from Apps.User.models import UserInfo, Grade, College, User, StudentInfo, WholeGrade, TeacherForGrade
# from Apps.Life.models import Building, Floor, Room, StuInRoom
# from Apps.Activity.models import Manage
from django.template import loader
from django.contrib.auth.models import Group, Permission
from Apps.Permission.models import *
from Apps.SchoolAttendance import models as SchoolAttendanceModels
from .tests import *
from django.contrib.contenttypes.models import ContentType
import time,datetime
# from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


def put_stu_room(stu, room,ret):
    """把学生放入寝室,注意第二个参数目前只支持xx#xxx形式"""
    history = StuInRoom.objects.filter(room=search_room(room), user=stu)
    try:
        if history.exists():
            ret.append("学生"+stu.userinfo.name+ "->"+ history.first().get_room()+ "已存在")
        else:
            room = search_room(room)
            stu_in_room = StuInRoom.objects.get_or_create(
                room=room, user=stu)
            ret.append("记录("+ "学号:"+ stu.username+ "姓名:"+ stu.userinfo.name+ "->"+stu_in_room[0].get_room()+ "寝室)已创建")
    except:
        ret.append(str(stu)+"异常")

def search_room(room_info):
    """xx#xxx解析"""
    try:
        building_name = room_info.strip().split("#")[0].strip()
        floor = room_info.strip().split("#")[1].strip()[0].strip()
        room = room_info.strip().split("#")[1].strip()[1:3].strip()
        building, flag = Building.objects.get_or_create(name=building_name)
        floor, flag = Floor.objects.get_or_create(building=building, name=floor)
        room, flag = Room.objects.get_or_create(name=room, floor=floor)
        return room
    except:
        return None


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


def import_stu_data(request):
    """寝室表导入"""
    file = request.data['file']
    work_book = load_workbook(file)
    ret = []
    for sheet in work_book:
        room_name = ""
        for info in sheet.values:
            if info[0] == "寝室日".strip():
                continue
            try:
                if info[0]:
                    room_name = str(info[0])[0:info[0].find("#") + 3 + 1]
                name = ''.join(re.findall('[\u4e00-\u9fa5]', str(info[2]))).strip()
                if len(name) == 0 or not name:
                    continue
                grade = str(info[3]).strip()
                stu_id = str(info[4]).strip()
                tel = str(info[5]).strip()
                user = User.objects.get_or_create(username=stu_id)
                user_info,flg0 = UserInfo.objects.get_or_create(
                    user=user[0])
                user_info.name = name
                user_info.tel = tel
                user_info.save()

                grade = Grade.objects.get_or_create(
                    name=grade)
                stu_info,flg1 = StudentInfo.objects.get_or_create(user=user[0],defaults={"grade":grade[0]})
                if not flg1:
                    stu_info.grade = grade[0]
                    stu_info.save()
                put_stu_room(user[0], room_name,ret)
            except User.DoesNotExist:
                ret.append(info[2]+name+"异常")
            except UserInfo.DoesNotExist:
                ret.append(info[2]+name+"异常")
            except:
                ret.append(info[2]+"---获取数据异常")

    return ret
# excel 转 列表 当第一个单元格为空是过滤这行数据
def excel_to_list(request):
    file = request.data['file']
    data = []
    wb = load_workbook(file,read_only=True)
    for rows in wb:
        for row in rows:#遍历行
            if row[0].value:
                l = []
                for i in row:
                    l.append(str(i.value))
                data.append(l)
    return data

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
            error = expand_permission.group_clean(group)
        # 根据flg的状态执行删除/添加
        elif group != None and username != None and flg != None:
            if flg == '+':
                # 组里面添加学生
                error = expand_permission.group_add_user(group,[username,])
            elif flg == '-':
                # pass
                error = expand_permission.group_remove_user(group,[username,])
                # 组里面删除学生
    ret['error'] = error
    return ret
# 导入学生
def user_init(request):
    ''' 导入学生'''
    message_list={}
    message_list['create'] = []
    message_list['update'] = []
    excel = excel_to_list(request)

    for row in excel:
        grade = row[0]
        username = row[1]
        name = row[2]
        
        # 创建/获取 班级
        grade,f0 = Grade.objects.get_or_create(name=grade)

        # 创建/获取 用户对象
        u,f = User.objects.get_or_create(username=username)
        if not u:
            continue
        u.set_password(username)
        u.save()

        # 创建/修改 用户 UserInfo StudentInfo
        user_info,f1 = UserInfo.objects.get_or_create(user=u, defaults={"name":name})
        stu_info,f2 = StudentInfo.objects.get_or_create(user=u, defaults={"grade":grade})

        # 记录结果
        if f1 and f2:
            message_list['create'].append(username+"---"+name)
        else:
            user_info.name = name
            user_info.save()
            stu_info.grade = grade
            stu_info.save()
            message_list['update'].append(username+"---"+name)
    return message_list

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
    d = expand_permission.group_init(names)
    ret = {
        "message":d,
        "names":names
    }
    return ret

# 用户寝室关联
def user_room(request):
    '''用户寝室关联'''
    rows = excel_to_list(request)
    message={}
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
                if username_ =="-":
                    room = search_room(room_)
                    room.stu_in_room.all().delete()
                    message['username-'].append(room_ + "：清空")

                # 学生寝室绑定/删除
                elif flg == '+':
                    user = User.objects.get(username=username_)
                    room = search_room(room_)
                    st,flg = StuInRoom.objects.get_or_create(user=user,defaults={"room":room})
                    st.room = room
                    st.save()
                    if flg:
                        message['flg+'].append(room_ + " 添加 " +  username_)
                    else:
                        message['update'].append(username_ + " 更新为 " +  room_)

                elif flg == '-':
                    user = User.objects.get(username=username_)
                    StuInRoom.objects.filter(user=user).delete()
                    message['flg-'].append(room_ + " 删除 " +  username_)
        except:
            print(username_)
            message['error'].append(username_)

    return message




def init_Attendance_group(request=None):
    '''考勤权限分组'''
    print('考勤权限分组')
    # 待添加进用户组的权限
    per1 = [
        '/api/school_attendance/task:GET',
        '/api/school_attendance/task:POST',

        '/api/school_attendance/task_admin:GET',
        '/api/school_attendance/task_admin:POST',
        '/api/school_attendance/task_admin:DELETE',

        '/api/school_attendance/task_switch:PUT',
        '/api/school_attendance/task_switch:DELETE',

        '/api/school_attendance/scheduling:GET',
        '/api/school_attendance/scheduling:POST',

        '/api/school_attendance/condition:GET',

        '/api/school_attendance/undo_record:DELETE',
    ]

    # 任务管理组
    name1 = 'task_admin'

    per2 = [
        '/api/school_attendance/in_zaoqian_excel:POST',
        '/api/school_attendance/undo_record_admin:DELETE',
    ]

    # 数据汇总组
    name2 = 'task_data'

    expand_permission.group_add_permission(name1,per1)
    expand_permission.group_add_permission(name2,per2)
    return 2000

def add_user():
    L = [
        ['195401', '19540140'],
        ['195303', '19530338'],
        ['195303', '19530345'],
    ]


# 生成考勤相关权限
def init_activity_permissions(request):
    '''
    初始化考勤权限管理模块
    '''
    ret = {'message': 'message', 'code': 2000}

    colleges = College.objects.all()
    # types =
    l = ('dorm', 'health', 'evening_study')

    for j in colleges:
        for i in l:

            # 初始化考勤任务管理表
            Manage.objects.get_or_create(
                types=i, college=j, code_name=j.code_name + "_" + i)

            p = Permission.objects.get_or_create(
                codename="manage-" + j.code_name + "_" + i,
                content_type=ContentType.objects.get_for_model(Manage),
                name=j.name+"_"+i
            )[0]
            g = Group.objects.get_or_create(
                name="manage_" + j.code_name + "_" + i)[0]
            g.permissions.clear()
            g.permissions.add(p)

            # 初始化考勤对应工作组
            p = Permission.objects.get_or_create(
                codename="work-" + j.code_name + "_" + i,
                content_type=ContentType.objects.get_for_model(Manage),
                name=j.name+"_"+i
            )[0]
            g = Group.objects.get_or_create(
                name="work_" + j.code_name + "_" + i)[0]
            g.permissions.clear()
            g.permissions.add(p)

        # 初始化晚自习工作组
        p = Permission.objects.get_or_create(
            codename=j.code_name+"_evening_study",
            content_type=ContentType.objects.get_for_model(Manage),
            name=j.name+"_"+i
        )[0]
        g = Group.objects.get_or_create(name=j.code_name+"_evening_study")[0]
        g.permissions.clear()
        g.permissions.add(p)

    # 楼层权限
    buildings = Building.objects.all()
    for i in l[:2]:
        for j in buildings:
            p = Permission.objects.get_or_create(
                codename="floor-"+i + "_" + j.name,
                content_type=ContentType.objects.get_for_model(Building),
                name=j.name+"号楼_"+i
            )[0]
            g = Group.objects.get_or_create(name=i + "_" + j.name)[0]
            g.permissions.clear()
            g.permissions.add(p)

    # 考勤管理员组
    expand_permission.group_init(['attendance_admin'])

    return JsonResponse(ret)




# 晚自修规则
def uinitialization_rules(request=None):
    '''晚自修规则
        codename:系统内部使用不能随意修改 导出Excel会使用
    '''
    print('晚自修规则初始化')
    # TODO 效率低
    rule_f = {
        'name':'查寝',
        'codename':'0#001',
        'is_person':True,
    }
    rule,flg = SchoolAttendanceModels.Rule.objects.get_or_create(**rule_f)
    rules = [
        {'name':'请假', 'score':'1', 'rule':rule},
        {'name':'未到校', 'score':'1', 'rule':rule},
        {'name':'当兵', 'score':'1', 'rule':rule},
    ]
    for r in rules:
        SchoolAttendanceModels.RuleDetails.objects.get_or_create(**r)
    # ----------------------------------------------------------------
    rule_f = {
        'name':'晚签',
        'codename':'0#002',
        'is_person':True,
    }
    rule,flg = SchoolAttendanceModels.Rule.objects.get_or_create(**rule_f)

    rules = [
        {'name':'旷一', 'score':'1', 'rule':rule},
        {'name':'旷二', 'score':'1', 'rule':rule},
    ]
    for r in rules:
        SchoolAttendanceModels.RuleDetails.objects.get_or_create(**r)
    # ----------------------------------------------------------------
    rule_f = {
        'name':'晚自修违纪',
        'codename':'0#003',
        'is_person':True,
    }
    rule,flg = SchoolAttendanceModels.Rule.objects.get_or_create(**rule_f)

    rules = [
        {'name':'睡觉', 'score':'1', 'rule':rule},
        {'name':'玩手机', 'score':'1', 'rule':rule},
    ]
    for r in rules:
        SchoolAttendanceModels.RuleDetails.objects.get_or_create(**r)
    # ---------------------------------------------------------------
    # 早签的名字修改 会影响早签数据批量导入和平台数据导出
    rule_f = {
        'name':'早签',
        'codename':'0#004',
        'is_person':True,
    }
    rule,flg = SchoolAttendanceModels.Rule.objects.get_or_create(**rule_f)

    rules = [
        {'name':'早签', 'score':'1', 'rule':rule},
    ]
    for r in rules:
        SchoolAttendanceModels.RuleDetails.objects.get_or_create(**r)
    # ---------------------------------------------------------------
    rule_f = {
        'name':'课堂',
        'codename':'0#005',
        'is_person':True,
    }
    rule,flg = SchoolAttendanceModels.Rule.objects.get_or_create(**rule_f)

    rules = [
        {'name':'早退', 'score':'1', 'rule':rule},
    ]

    for r in rules:
        SchoolAttendanceModels.RuleDetails.objects.get_or_create(**r)

    return {"code":2000}


class In_zaoqian_excel(APIView):

    def post(self,request):
        """针对寝室表"""
        file = request.data['file']

        file_name = str(time.time())+ '__' +file.name
        file_path = os.path.join('upload', file_name)
        f = open(file_path,'wb')
        for i in file.chunks():   #chunks方法是一点点获取上传的文件内容
            f.write(i)
        f.close()

        file_name = 'upload//' + file_name

        # return JsonResponse({})
        
        wb = load_workbook(file,read_only=True)

        error_list=[]
        for rows in wb:
            for row in rows:#遍历行
                username = row[0].internal_value
                name = row[1].internal_value
                str_time = row[3].internal_value
                is_header = username.find('考勤') != -1 or username.find('统计') != -1 or username.find('员工号') != -1
                if not (username == None or name == None or str_time == None) and not is_header:
                    print(username)
                    try:
                        u = User.objects.get(username=username)
                        try:
                            str_time = datetime.datetime.strptime(str_time,'%Y/%m/%d')
                            d = {
                                'rule_str':'旷早签',
                                'student_approved':u,
                                'score':1,
                                'star_time':str_time
                            }
                            sa,flg = SchoolAttendanceModels.Record.objects.get_or_create(**d)
                            sa.worker =  request.user
                            sa.save()
                        except:
                            error_list.append({
                                'username':username,
                                'name':name,
                                'str_time':str_time,
                                'message':'导入记录失败'
                            })
                    except:
                        error_list.append({
                            'username':username,
                            'name':name,
                            'str_time':str_time,
                            'message':'用户不存在'
                        })

        ret = {
            'message': '添加成功 请检查添加结果',
            'code':'2000',
            'data':error_list
        }
        return JsonResponse(ret)
        


class DataInit(APIView):
    """系统数据初始化"""

    def post(self, request):
        init_dict = {
            # 用户组初始化
            "group_init":group_init,
            # 晚自修规则
            "uinitialization_rules":uinitialization_rules,
            # 考勤权限分组
            "init_Attendance_group":init_Attendance_group,
            # 导入学生
            "user_init":user_init,
            # 用户寝室关联
            "user_room":user_room,
            # 寝室表导入
            "import_stu_data":import_stu_data,
            # 用户与组的管理
            "group_user":group_user,
        }
        type_ = request.data['type']
        data = init_dict[type_](request)
        return JsonResponse(data, safe=False)