"""audit管理"""
import datetime
from Apps.Ask import ser
from Apps.Ask.models import Audit, Ask
from Apps.Ask.utils.exceptions import *
from Apps.User.models import TeacherForCollege, Grade


class AuditOperate(object):
    """对Audit操作"""

    def __init__(self, request, ask_id):
        if ask_id is None:
            raise AuditException("没有请假条id")
        self._ask = Ask.objects.get(id=ask_id)
        self._audit = Audit.objects.none()
        self._request = request

    def view(self, audit_id):
        """查看"""
        try:
            self._audit = Audit.objects.get(id=audit_id)
            return ser.AuditSerializer(self._audit).data
        except Audit.DoesNotExist:
            return False

    @staticmethod
    def views(user, class_id):
        """查看关于用户/此用户进行的审批记录"""
        return ser.AuditSerializer(instance=Audit.objects.filter(
            approve_teacher=user, user__studentinfo__grade=int(class_id)), many=True).data

    def audit(self, decide=""):
        """审核"""
        if decide == "passed":
            AskAudit(self._request.user, self._ask).pass_audit()
        elif decide == "failed":
            AskAudit(self._request.user, self._ask).un_pass_audit()
        else:
            if self._ask.status == "first_audit":
                FirstAudit(self._request.user, self._ask).audits()
            elif self._ask.status == "second_audit":
                SecondAudit(self._request.user, self._ask).audits()
            elif self._ask.status == "college_audit":
                CollegeAudit(self._request.user, self._ask).audits()
            elif self._ask.status == "university_audit":
                UniversityAudit(self._request.user, self._ask).audits()
            else:
                raise AlreadyAuditException("请假条审批已完成")
        return True


class AskAudit(object):
    """审核基类"""
    _hours = 0

    def __init__(self, user, ask):
        self._ask = ask
        self._user = user

    def pass_audit(self, explain=""):
        return self._pass_audit(explain)

    def un_pass_audit(self, explain=""):
        return self._un_pass_audit(explain)

    def audits(self, explain=""):
        pass

    def _pass_audit(self, explain=""):
        # 续假通过,把续假的时间改回去
        if self._ask.end_time != self._ask.extra_end_time:
            self._ask.end_time = self._ask.extra_end_time
        self._ask.status = "passed"
        self._ask.save()
        self._add_record(self._ask.status, explain)
        return True

    def _un_pass_audit(self, explain=""):
        # 续假不通过就要把时间改回去
        if self._ask.end_time != self._ask.extra_end_time:
            self._ask.end_time, self._ask.extra_end_time = self._ask.extra_end_time, self._ask.end_time
        self._ask.status = "failed"
        self._ask.save()
        self._add_record(self._ask.status, explain)
        return True

    def _add_record(self, status, explain):
        audit = Audit.objects.create(
            user=self._user, ask=self._ask,
            status=status, explain=explain,
            modify_time=datetime.datetime.now(),
            approve_teacher=self._user
        )
        audit.save()
        return True


class FirstAudit(AskAudit):
    """审核第一步,给班主任审核"""

    def __init__(self, user, ask):
        super().__init__(user, ask)
        self.__user = user
        self.__ask = ask

    def audits(self, explain=""):
        print("班主任审批并提交")
        self.__ask.status = "second_audit"
        __next_pass_user = self.__ask.grade.whole_grade.user
        if __next_pass_user:
            self.__ask.approve_user = __next_pass_user
            self.__ask.save()
            self._add_record(self.__ask.status, explain)
            return True
        else:
            raise NextAuditException("无法找到班级相关的辅导员")


class SecondAudit(AskAudit):
    """第二步,辅导员审核"""

    def __init__(self, user, ask):
        super().__init__(user, ask)
        self.__user = user
        self.__ask = ask

    def audits(self, explain=""):
        print("辅导员审核")
        self.__ask.status = "college_audit"
        college = self.__ask.grade.college
        try:
            self.__ask.approve_user = TeacherForCollege.objects.get(college=college).user
        except TeacherForCollege.DoesNotExist:
            raise NextAuditException("该分院没有设置领导")
        self.__ask.save()
        self._add_record(self.__ask.status, explain)
        return True


class CollegeAudit(AskAudit):
    """可选,院级审核"""

    def __init__(self, user, ask):
        super().__init__(user, ask)
        self.__user = user
        self.__ask = ask

    def audits(self, explain=""):
        print("院级审核")
        self.__ask.status = "university_audit"
        self._add_record(self.__ask.status, explain)
        if not self.__ask.grade.college:
            head_teacher = TeacherForCollege.objects.get(college=self.__ask.grade.college).user
            self.__ask.approve_user = head_teacher
            self.__ask.save()
            return True
        raise NextAuditException("该班级没有分配学院")


class UniversityAudit(AskAudit):
    """可选,校级审核"""

    def __init__(self, user, ask):
        super().__init__(user, ask)
        self.__user = user
        self.__ask = ask

    def audits(self, explain=""):
        raise NextAuditException("校级审核请选择过或不过(没有下一级的审批了)")
