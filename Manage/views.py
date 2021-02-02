'''管理视图'''
import logging
from django.http import JsonResponse
from rest_framework.views import APIView
# from openpyxl import load_workbook
from Apps.User.models import UserInfo,User
from django.contrib.auth.models import User as djangoUser
from Apps.Life.models import Building,Room,Floor,StuInRoom
# Create your views here.
from Apps.Permission.utils.auth import AuthPer,AuthPermission
logger = logging.getLogger(__name__)
class Test(APIView):
    # authentication_classes = [AuthPer,]
    '''后台接口调用'''
    def get(self,request):
        '''测试接口'''
        print('视图 当前User：',request.user)
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
        # user = User(user_name="19530200",pass_word="123456",django_user=djangoUser.objects.get(username="19530200"))
        # user.save()
        return JsonResponse({"message":"out"})

def manual_add_stuinroom(userid,roominfo):
    '''手动添加入住信息'''
    user = User.objects.filter(user_name=userid)
    if user.exists():
        room = serach_room(roominfo)
        StuInRoom(stuid=user.first(),roomid=room).save()
        print("用户:",user,"->",room,"已添加")
    else:
        print("没有此用户")

def put_stu_inroom(name,room,log):
    '''把学生放入寝室,注意第二个参数目前只支持xx#xxxd形式'''
    student_list = UserInfo.objects.filter(name=name.strip())
    if not student_list.exists():
        log.write("学生:"+name+" 不存在\n")
        print("学生",name,"不存在")
    elif student_list.count()>1:
        log.write("学生:"+name+" 存在同名\n")
        print("学生",name,"存在同名")
        log.write("学生 "+name+" 存在同名\n")
        for student in student_list:
            stuinroom = StuInRoom.objects.filter(stuid=student.user_id)
            if stuinroom.exists():
                print("学生:",student.name,"学号:",student.user_id.user_name,"已住寝:",stuinroom)
                log.write(
                    "学生: "+student.name+" 学号: "+student.user_id.user_name+"已住寝: "+
                    stuinroom.name+"\n"
                    )
            else:
                print("学生:",student.name,"学号:",student.user_id.user_name,"未住寝")
                log.write("学生: "+student.name+" 学号: "+student.user_id.user_name+" 未住寝\n")
    elif student_list.count() == 1:
        student = student_list.first()
        history = StuInRoom.objects.filter(roomid=serach_room(room),stuid=student.user_id)
        if history.exists():
            print("学生",student.name,"->",history.first(),"已存在")
            # log.write("学生 "+student.name+" -> "+ str(history.first())+" 已存在\n")
        else:
            room = serach_room(room)
            stuinroom = StuInRoom(roomid = room,stuid=student.user_id)
            stuinroom.save()
            print("记录(","学号:",student.user_id.user_name,"姓名:",student.name,"->",stuinroom,"寝室)已创建")
            # log.write(
            #     "记录("+"学号: "+student.user_id.user_name+" 姓名: "+
            #     student.name+" -> "+
            #     str(stuinroom)+"寝室)已创建\n"
            #     )
    else:
        print("filter发生错误,它的结果既不是0,也不是1,也不是大于1,请检查代码!")

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
