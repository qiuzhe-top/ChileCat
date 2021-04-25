"""根据权限处理请假条"""
import os
import datetime
from django.contrib.auth.models import AnonymousUser
from Apps.Ask import ser
from Apps.Ask.models import Ask
from Apps.Ask.utils.exceptions import AskAddTimeException, AskViewException
from Apps.User.models import StudentInfo
from docxtpl import DocxTemplate

COMPLETED = {"passed", "failed"}
UNCOMPLETED = {"draft", "first_audit", "second_audit", "college_audit", "university_audit"}


class AskOperate(object):
    """请假条操作"""
    _user = AnonymousUser
    _ask_list = Ask.objects.none()  # <QuerySet[]>

    def __init__(self, user):
        self._user = user

    def view(self, ask_id=-1, view_type=None, identity=None):
        """查看请假条"""
        if ask_id != -1:
            self._ask_list = Ask.objects.get(id=ask_id)
            return ser.AskSerializer(instance=self._ask_list).data
        else:
            ask_list = "身份异常-尝试查看请假条"

            if identity:
                if identity == "teacher":
                    ask_list = {'list': AskToTeacher(self._user).views()}
                elif identity == "monitor":
                    ask_list = {'list': MonitorAsk(self._user).views(view_type)}
            else:
                ask_list = {'list': AskToStudent(self._user).views(view_type)}
            if not self._ask_list:
                self._ask_list = ask_list
        return self._ask_list

    def delete(self, ask_id):
        """删除请假条"""
        self._ask_list = Ask.objects.get(id=ask_id)
        self._ask_list.delete()
        return True

    def statistics(self):
        """统计请假"""
        self._ask_list = Ask.objects.all()
        return ser.AskSerializer(instance=self._ask_list, many=True).data

    @staticmethod
    def export_word(ask_id):
        """输出到word"""
        ask = Ask.objects.get(id=int(ask_id))
        room = ask.user.stu_in_room.first()
        today = datetime.date.today()
        path = os.getcwd()
        doc = DocxTemplate(path+"\\Apps\\Ask\\utils\\学生请假离校审批表.docx")
        context = {'info': {
            'name': ask.user.userinfo.name,
            'tel': ask.contact_info or "",
            'no': ask.user.username,
            'gender': ask.user.userinfo.gender,
            'college': ask.grade.college.name,
            'room': room,
            'reason': ask.reason,
            'place': ask.place,
            'start_time': ask.start_time,
            'end_time': ask.end_time,
        },
            'date': {
                'year': today.year,
                'month': today.month,
                'day': today.day,
            }
        }
        doc.render(context)
        return doc


class AskToTeacher(AskOperate):
    """
    老师->请假条
    """

    def views(self):
        print("老师查看请假条:")
        if self._user.get.has_perm("operate-ask_teacher_view"):
            self._ask_list = Ask.objects.filter(approve_user=self._user, status="first_audit")
            return ser.AskSerializer(instance=self._ask_list, many=True).data
        raise AskViewException('没有权限:"以老师身份查看请假条!"')


class AskToStudent(AskOperate):
    """
    学生->请假条
    """

    def __init__(self, user):
        super().__init__(user)
        self._user = user

    def views(self, audit_type):
        """
        学生查看请假条
        0表示审核中,1表示完成
        """
        print("学生查看请假条,type =", audit_type)
        self._ask_list = Ask.objects.filter(user_id=self._user)
        if audit_type:
            __status = COMPLETED if audit_type == "1" else UNCOMPLETED
            self._ask_list = self._ask_list.filter(user_id=self._user, status__in=__status)
        return ser.AskAbbrSerializer(instance=self._ask_list, many=True).data

    def submit(self, ask_info):
        """学生提交请假条"""
        ask_info['user'] = self._user
        ser.AskAntiSerializer(Ask).create(ask_info)
        return True

    def modify(self, ask_id, validated_data):
        """学生修改请假条"""
        # 如果是续假
        extra_end_time = validated_data.get('time_back', None)
        print("续假:", extra_end_time)
        if extra_end_time:
            return self.__add_time(ask_id, extra_end_time)
        self._ask_list = Ask.objects.get(id=ask_id)
        ser.AskAntiSerializer(Ask).update(self._ask_list, validated_data)
        return True

    def __add_time(self, ask_id, extra_end_time):
        """续假"""
        self._ask_list = Ask.objects.get(id=ask_id)
        if self._ask_list.status not in COMPLETED:
            raise AskAddTimeException("此请假条不能续假")
        print(self._ask_list.end_time, extra_end_time)
        if self._ask_list.extra_end_time >= datetime.datetime.strptime(extra_end_time, "%Y-%m-%d %H:%M"):
            raise AskAddTimeException("续假时间太短")
        self._ask_list.extra_end_time = extra_end_time
        # 把续假时间变成普通的审核时间，再重新交给班主任审核
        self._ask_list.end_time, self._ask_list.extra_end_time = self._ask_list.extra_end_time, self._ask_list.end_time
        self._ask_list.status = "first_audit"
        self._ask_list.save()
        return True


class MonitorAsk(AskOperate):
    """班委"""

    def __init__(self, user):
        super().__init__(user)
        self.__user = user

    def views(self, audit_type=None):
        print("班委查看请假条")
        # 判断班委的条件
        if self.__user.has_perm("operate-ask_monitor_view"):
            grade = StudentInfo.objects.get(user=self._user).grade
            today = datetime.datetime.today()
            fifteen_ago = today - datetime.timedelta(days=15)
            self._ask_list = Ask.objects.filter(grade=grade, start_time__gte=fifteen_ago)
            if audit_type:
                __status = COMPLETED if audit_type == "1" else UNCOMPLETED
                self._ask_list = self._ask_list.filter(grade=grade, status__in=__status)
            return ser.AskAbbrSerializer(instance=self._ask_list, many=True).data
        raise AskViewException('没有权限:以班委身份查看请假条!')
