'''管理视图'''
import logging
import re
# from django.contrib.auth.models import User
from django.http import JsonResponse
from openpyxl import load_workbook
from rest_framework.views import APIView
# from django.contrib.auth.models import User as djangoUser
# from django.db.models import Q
from Apps.Permission.utils import expand_permission
from Apps.User.models import UserInfo,Grade,College,User,StudentInfo
from Apps.Life.models import Building, Floor, Room, StuInRoom
from Apps.Ask.utils.ask import AskToTeacher,AskToStudent,AskOperate
from Apps.Ask.models import Ask
from Apps.Ask.ser import AskSerializer

logger = logging.getLogger(__name__)
class Test(APIView):
    '''后台接口调用'''
    def get(self,request):
        '''测试接口'''
        print('视图 当前User：',request.user)
        tea = AskToTeacher(User.objects.get(username="admin"))
        print(User.objects.get(username="admin").groups.filter(name="teacher").exists())
        # import_student("leaksfile//stu20.xlsx",0)#只能针对 id 班级 学号 姓名 这样的表格
        # import_studata("leaksfile//副本智慧交通学院学生寝室信息表（全).xlsx")
        # excel_file = "leaksfile//roomnumbers//all.xlsx"
        # workbook = load_workbook(excel_file)
        # log = open(excel_file+".log","w")
        # serach_room("1#101")
        # for sheet in workbook:
        #     for row in sheet.values:
        #         # print(row[0].strip(),row[1].strip())
        #         pass
        #         # put_stu_inroom(row[0].strip(),row[1].strip(),log)
        # log.close()

        # user_list = User.objects.all()
        # for user in user_list:
        #     user.django_user = djangoUser.objects.get(username=user.user_name)
        #     user.save()
        #     print(user.django_user)
        # user = User(
        #     user_name="19530200",pass_word="123456",
        #     django_user=djangoUser.objects.get(username="19530200")
        #     )
        # user.save()
        return JsonResponse({"message":tea.view()})

def manual_add_stuinroom(userid,roominfo):
    '''手动添加入住信息'''
    user = User.objects.filter(user_name=userid)
    if user.exists():
        room = serach_room(roominfo)
        StuInRoom(stuid=user.first(),roomid=room).save()
        print("用户:",user,"->",room,"已添加")
    else:
        print("没有此用户")

def put_stu_inroom(stu,room,log):
    '''把学生放入寝室,注意第二个参数目前只支持xx#xxxd形式'''
    student = stu
    history = StuInRoom.objects.filter(roomid=serach_room(room),stuid=student)
    if history.exists():
        print("学生",student.userinfo.name,"->",history.first(),"已存在")
    #     # log.write("学生 "+student.name+" -> "+ str(history.first())+" 已存在\n")
    else:
        room = serach_room(room)
        stuinroom = StuInRoom.objects.get_or_create(roomid=room,stuid=student)
        # stuinroom = StuInRoom(roomid = room,stuid=student)
        # stuinroom.save()
        print("记录(","学号:",student.username,"姓名:",student.userinfo.name,"->",stuinroom[0],"寝室)已创建")
        # log.write(
        #     "记录("+"学号: "+student.user_id.user_name+" 姓名: "+
        #     student.name+" -> "+
        #     str(stuinroom)+"寝室)已创建\n"
        #     )

def serach_room(roominfo):
    '''xx#xxx解析'''
    budid = roominfo.strip().split("#")[0].strip()
    floorid = roominfo.strip().split("#")[1].strip()[0].strip()
    roomid = roominfo.strip().split("#")[1].strip()[1:3].strip()
    budling = Building.objects.filter(budnum=budid)
    if not budling.exists():
        # print(budid,"号楼不存在,准备创建")
        created_building = Building(budnum=budid)
        created_building.save()
        print(created_building,"号楼创建完毕")
        budling = created_building
    else:
        budling = budling.first()
    floor = Floor.objects.filter(budid=budling,floornum=floorid)
    if not floor.exists():
        # print(budling,"号楼",floorid,"层不存在,准备创建")
        created_floor = Floor(budid=budling,floornum=floorid)
        created_floor.save()
        print(created_floor,"层创建完毕")
        floor = created_floor
    else:
        floor = floor.first()
    room = Room.objects.filter(roomnum=roomid,floor=floor)
    if not room.exists():
        # print(floor,roomid,"房间不存在,准备创建")
        created_room = Room(roomnum=roomid,floor=floor)
        created_room.save()
        print(created_room,"房间创建完毕")
        room = created_room
    else:
        room = room.first()
    return room

def import_student(file,log):
    '''
    学生账号(学号)密码(123456)导入
    file:xlsx文件名(包含路径)
    log:输出日志路径
    '''
    # 序号 班级 学号 姓名
    print(log)
    num = 0
    work_book = load_workbook(file)
    for sheet in work_book:
        for info in sheet.values:
            # (1,xxx,xxx,xxx)
            grade = str(info[1]).strip()
            user_id = str(info[2]).strip()
            name = str(info[3]).strip()
            print(grade,user_id,name)
            if not User.objects.filter(username=user_id).exists():
                user = User(username=user_id,password="123456")
                user.save()
            else:
                user = User.objects.get(username=user_id)
            if not UserInfo.objects.filter(user_id=user,name=name).exists():
                userinfo = UserInfo(user_id=user,name=name)
                userinfo.save()
            else:
                userinfo = UserInfo.objects.get(user_id=user,name=name)
            if not Grade.objects.filter(name=grade).exists():
                grade = create_class(grade,"智慧交通学院")
                grade.save()
            else:
                grade = Grade.objects.get(name=grade)
            if not StudentInfo.objects.filter(user_id=user).exists():
                stuinfo = StudentInfo(user_id=user,grade_id=grade)
                stuinfo.save()
            num += 1
    print(num,"个记录添加完毕")

def create_class(class_name,college_name):
    '''创建班级'''
    if not Grade.objects.filter(name=class_name).exists():
        if not College.objects.filter(name=college_name).exists():
            college = College(name=college_name)
            college.save()
            print("分院:",college,"创建.")
        college = College.objects.get(name=college_name)
        grade = Grade(name = class_name,college_id=college)
        grade.save()
        print("班级",grade,"创建")
        return grade
    print("班级已存在,无需创建!")
    return None

def import_studata(file):
    """针对寝室表"""
    work_book = load_workbook(file)
    log = open(file+".log","w")
    for sheet in work_book:
        room_name = ""
        for info in sheet.values:
            if info[0] == "寝室日".strip():
                continue
            if info[0]:
                room_name = str(info[0])[0:info[0].find("#")+3+1]
            name = ''.join(re.findall('[\u4e00-\u9fa5]',str(info[2]))).strip()
            grade = str(info[6]).strip()
            stu_id = str(info[7]).strip()
            tel = str(info[8]).strip()
            try:
                user = User.objects.get_or_create(username=stu_id,password="123456")
                userinfo = UserInfo.objects.get_or_create(user_id=user[0],name=name,tel=tel)
                college = College.objects.get_or_create(name="智慧交通学院")
                grade = Grade.objects.get_or_create(name=grade,college_id=college[0])
                stu_info = StudentInfo.objects.get_or_create(user_id=user[0],grade_id=grade[0])
                put_stu_inroom(user[0],room_name,log)
            except User.DoesNotExist:
                print(name,grade,stu_id,tel)
            except UserInfo.DoesNotExist:
                print(name,grade,stu_id,tel)

class ApiPer(APIView):
    '''权限测试'''
    def get(self, request):
        """test"""
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        expand_permission.init_api_permissions()
        # expand_permission.init_operate_permissions()
        # ret['data'] = data
        p = request.user.get_all_permissions()
        d2 = [x[11:] for x in p if x.find('OPERATE')!= -1 ]
        print(d2)
        return JsonResponse(ret)
