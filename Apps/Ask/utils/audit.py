"""audit管理"""
import datetime
from Apps.Ask import ser
from Apps.Ask.models import Audit
from Apps.Ask.utils.exceptions import *
from Apps.User.models import TeacherForWholeGrade, TeacherForCollege


class AuditOperate(object):
    """对Audit操作"""

    def __init__(self, request, ask):
        self._ask = ask
        self._audit = Audit.objects.none()
        self._request = request

    def view(self, audit_id):
        """查看"""
        try:
            self._audit = Audit.objects.get(id=audit_id)
            return ser.AuditSerializer(self._audit).data
        except Audit.DoesNotExist:
            return False

    def views(self, user):
        """查看关于用户/此用户进行的审批记录"""

    def audits(self):
        """审核"""

    def create_record(self):
        """创建审批记录"""


class AskAudit(object):
    """审核基类"""
    _hours = 0

    def __init__(self, user, ask):
        self._ask = ask
        self._user = user
        self._hours = (self._ask.end_time - self._ask.start_time).seconds / 3600
        if self._ask.pass_id != self._user:
            raise AuthAuditException("你没有审批此请假条的权限")

    def audit(self, explain=""):
        pass

    def _pass_audit(self, explain=""):
        self._ask.status = "passed"
        self._ask.save()
        self._add_record(self._ask.status, explain)
        return True

    def _unpass_audit(self, explain=""):
        self._ask.status = "failed"
        self._ask.save()
        self._add_record(self._ask.status, explain)
        return True

    def _add_record(self, status, explain):
        audit = Audit.objects.create(
            user_id=self._user, ask_id=self._ask,
            status=status, explain=explain,
            modify_time=datetime.datetime.now()
        )
        audit.save()
        return True


class FirstAudit(AskAudit):
    """审核第一步,给班主任审核"""

    def __init__(self, user, ask):
        super().__init__(user, ask)
        self.__user = user
        self.__ask = ask

    def audit(self, explain=""):
        self.__ask.status = "scored_audit"
        self.__ask.save()
        self._add_record(self.__ask.statu, explain)
        # TODO 交给辅导员
        return True


class SecondAudit(AskAudit):
    """第二步,辅导员审核"""

    def __init__(self, user, ask):
        super().__init__(user, ask)
        self.__user = user
        self.__ask = ask

    def audit(self, explain=""):
        # TODO 超过72小时(3天)给院级
        if self._hours > 72:
            self.__ask.status = "college_audit"
            self._add_record(self.__ask.status, explain)
            # TODO 交给院级领导审核
        else:
            self._pass_audit(explain)


class CollegeAudit(AskAudit):
    """可选,院级审核"""

    def __init__(self, user, ask):
        super().__init__(user, ask)
        self.__user = user
        self.__ask = ask

    def audit(self, explain=""):
        # TODO 超过168小时(7天)教给校级
        if self._hours > 168:
            self.__ask.status = "university_audit"
            self._add_record(self.__ask.status, explain)
            # TODO 交给校级审批
        else:
            self._pass_audit(explain)


class UniversityAudit(AskAudit):
    """可选,校级审核"""

    def __init__(self, user, ask):
        super().__init__(user, ask)
        self.__user = user
        self.__ask = ask

    def audit(self, explain=""):
        raise NextAuditException("校级审核请选择过或不过(没有下一级的审批了)")
