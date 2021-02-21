"""根据权限处理请假条"""
import datetime
from django.contrib.auth.models import AnonymousUser
from Apps.Ask import ser
from Apps.Ask.models import Ask
from Apps.Ask.utils.exceptions import AskAddTimeException
from Apps.User.models import StudentInfo

COMPLETED = {"passed", "failed"}
UNCOMPLETED = {"draft", "first_audit", "scored_audit", "college_audit", "university_audit"}


class AskOperate(object):
    """操作主类"""
    _user = AnonymousUser
    _ask_list = Ask.objects.none()  # <QuerySet[]>

    def __init__(self, user):
        self._user = user

    def view(self, ask_id=-1, view_type=None, monitor=None):
        """目的:查看单条"""
        try:
            if ask_id != -1:
                self._ask_list = Ask.objects.get(id=ask_id)
                return ser.AskSerializer(instance=self._ask_list).data
            else:
                if self._user.groups.filter(name="teacher").exists():
                    ask_list = {'list': AskToTeacher(self._user).views()}
                else:
                    if monitor:
                        ask_list = {'list': MonitorAsk(self._user).views(view_type)}
                    else:
                        ask_list = {'list': AskToStudent(self._user).views(view_type)}
            if not self._ask_list:
                self._ask_list = ask_list
            return self._ask_list
        except Ask.DoesNotExist as ask_un_exist:
            raise ask_un_exist

    def delete(self, ask_id):
        """删除请假条"""
        try:
            self._ask_list = Ask.objects.get(id=ask_id)
            self._ask_list.delete()
        except Ask.DoesNotExist as ask_not_exist:
            return ask_not_exist
        return True


class AskToTeacher(AskOperate):
    """
    老师->请假条
    """

    def views(self):
        print("老师查看请假条")
        AskOperate._ask_list = Ask.objects.filter(pass_id=self._user)
        return ser.AskAbbrSerializer(instance=AskOperate._ask_list, many=True).data


class AskToStudent(AskOperate):
    """
    学生->请假条
    """

    def __init__(self, user):
        super().__init__(user)

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

    def submit(self, ask_id):
        """学生提交请假条"""
        try:
            self._ask_list = Ask.objects.get(id=ask_id)
            ser.AskAntiSerializer(Ask).update(self._ask_list, {'status': "first_audit"})
            return True
        except Ask.DoesNotExist as ask_not_exist:
            print(ask_not_exist)
            return ask_not_exist

    def modify(self, ask_id, validated_data):
        """学生修改请假条"""
        # 如果是续假
        if validated_data.get('extra_time', False):
            return self.__add_time(ask_id)
        try:
            self._ask_list = Ask.objects.get(id=ask_id)
            ser.AskAntiSerializer(Ask).update(self._ask_list, validated_data)
            return True
        except Ask.DoesNotExist as ask_not_exist:
            print(ask_not_exist)
            return ask_not_exist

    def __add_time(self, ask_id):
        """续假"""
        # TODO 续假
        self._ask_list = Ask.objects.get(id=ask_id)
        if self._ask_list.end_time == self._ask_list.extra_end_time:
            raise AskAddTimeException("续假时间为0")
        # 把续假时间变成普通的审核时间，再重新交给班主任审核
        self._ask_list.end_time, self._ask_list.extra_end_time = self._ask_list.extra_end_time, self._ask_list.end_time
        self._ask_list.status = "first_audit"
        self._ask_list.save()
        return True


class MonitorAsk(AskOperate):
    """班委"""

    def views(self, audit_type=None):
        print("班委查看请假条")
        # TODO 班委
        grade = StudentInfo.objects.get(user_id=self._user).grade_id
        today = datetime.datetime.today()
        fifteen_ago = today - datetime.timedelta(days=15)
        self._ask_list = Ask.objects.filter(grade_id=grade, start_time__gte=fifteen_ago)
        if audit_type:
            __status = COMPLETED if audit_type == "1" else UNCOMPLETED
            self._ask_list = self._ask_list.filter(grade_id=grade, status__in=__status)
        return ser.AskAbbrSerializer(instance=self._ask_list, many=True).data
