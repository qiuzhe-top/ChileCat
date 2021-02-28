"""管理视图"""
import logging
import re
from django.http import JsonResponse, HttpResponse
from openpyxl import load_workbook
from rest_framework.views import APIView
from Apps.Permission.utils import expand_permission
from Apps.User.models import UserInfo, Grade, College, User, StudentInfo, WholeGrade, TeacherForGrade
from Apps.Life.models import Building, Floor, Room, StuInRoom
from django.template import loader
from Apps.Permission.models import *
from django.contrib.contenttypes.models import ContentType
from docxtpl import DocxTemplate
from .tests import *

logger = logging.getLogger(__name__)


class Test(APIView):
    """后台接口调用"""

    def get(self, request):
        """测试接口"""
        print("GET参数:", self.request.query_params)
        print("request data:", self.request.data)
        print("TOKEN:", self.request.META.get("HTTP_TOKEN"))
        print('测试接口')
        pers = Permission.objects.all()
        for per in pers:
            if per.codename[0:4]=="/api":
                per.delete()
        # 班级改小写
        # grades = Grade.objects.all()
        # for grade in grades:
        #     if grade.name != grade.name.lower():
        #         grade.name = grade.name.lower()
        #         grade.save()

        # print("创建班主任:")
        # grades = Grade.objects.all()
        # for grade in grades:
        #     grade_name = grade.name
        #     teacher_username = grade_name + "00"
        #     teacher, flag = User.objects.get_or_create(username=teacher_username)
        #     teacher.set_password("123456")
        #     teacher.save()
        #     UserInfo.objects.get_or_create(user=teacher, name=grade_name+"班老师", identity="teacher")
        #     print(TeacherForGrade.objects.get_or_create(user=teacher, grade=grade))
        # import_stu_data("leaksfile//副本智慧交通学院学生寝室信息表（全).xlsx")
        return JsonResponse({"message": ""})


def put_stu_room(stu, room, log):
    """把学生放入寝室,注意第二个参数目前只支持xx#xxx形式"""
    student = stu
    history = StuInRoom.objects.filter(room=search_room(room), student=student)
    if history.exists():
        print("学生", student.userinfo.name, "->", history.first(), "已存在")
    else:
        room = search_room(room)
        stu_in_room = StuInRoom.objects.get_or_create(room=room, student=student)
        print("记录(", "学号:", student.username, "姓名:", student.userinfo.name, "->", stu_in_room[0], "寝室)已创建")


def search_room(room_info):
    """xx#xxx解析"""
    building_name = room_info.strip().split("#")[0].strip()
    floor = room_info.strip().split("#")[1].strip()[0].strip()
    room = room_info.strip().split("#")[1].strip()[1:3].strip()
    building, flag = Building.objects.get_or_create(name=building_name)
    floor, flag = Floor.objects.get_or_create(building=building, name=floor)
    room, flag = Room.objects.get_or_create(name=room, floor=floor)
    return room


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


def import_stu_data(file):
    """针对寝室表"""
    work_book = load_workbook(file)
    log = open(file + ".log", "w")
    for sheet in work_book:
        room_name = ""
        for info in sheet.values:
            if info[0] == "寝室日".strip():
                continue
            if info[0]:
                room_name = str(info[0])[0:info[0].find("#") + 3 + 1]
            name = ''.join(re.findall('[\u4e00-\u9fa5]', str(info[2]))).strip()
            grade = str(info[6]).strip()
            stu_id = str(info[7]).strip()
            tel = str(info[8]).strip()
            try:
                user = User.objects.get_or_create(username=stu_id)
                UserInfo.objects.get_or_create(user=user[0], name=name, tel=tel)
                college = College.objects.get_or_create(name="智慧交通学院")
                grade = Grade.objects.get_or_create(name=grade, college=college[0])
                StudentInfo.objects.get_or_create(user=user[0], grade=grade[0])
                put_stu_room(user[0], room_name, log)
            except User.DoesNotExist:
                print(name, grade, stu_id, tel)
            except UserInfo.DoesNotExist:
                print(name, grade, stu_id, tel)


class ApiPer(APIView):
    """权限测试"""

    def get(self, request):
        """test"""
        ret = {'message': 'message', 'code': 2000}
        urls = expand_permission.get_all_url_dict()
        # print(urls)
        # for url, detail in urls.items():
        #     print("url:", url, "备注:", detail)
        #     if detail:
        #         for method in detail['method']:
        #             per = Permission.objects.get_or_create(
        #                 codename=url + ":" + method, name=detail['name'][1],
        #                 content_type_id=ContentType.objects.get_for_model(ApiPermission).id
        #             )
        #             print(per)
        #             ApiPermission.objects.get_or_create(permission=per[0])
        # expand_permission.init_api_permissions()
        # self.request.user = User.objects.get(username="19530226")
        # expand_permission.init_operate_permissions()
        # ret['data'] = data
        # p = self.request.user.get_all_permissions()
        # d2 = [x[11:] for x in p if x.find('OPERATE') != -1]
        # print(d2)
        return JsonResponse(ret)


class Index(APIView):
    """"""

    def get(self, request):
        api_permission_list = ApiPermission.objects.filter(
            permission__codename="/api/life/idcode:GET").values_list('permission__codename', flat=True)
        urls = []
        id_code = "api/life/idcode"
        for api in api_permission_list:
            ap = str(api).split(":")
            urls.append(ap[0])
        template = loader.get_template('Manage/index.html')
        context = {
            'display_list': api_permission_list,
            'id_code': id_code,
        }
        return HttpResponse(template.render(context, request))
