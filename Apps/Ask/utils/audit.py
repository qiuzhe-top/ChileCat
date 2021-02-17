"""audit管理"""
from Apps.Ask import ser
from Apps.Ask.models import Audit


class AuditOperate:
    """对Audit操作"""
    _audit = Audit.objects.none()

    # TODO(liuhai) 暂时缺什么补什么
    def view(self, audit_id):
        """查看"""
        try:
            self._audit = Audit.objects.get(id=audit_id)
            return ser.AuditSerializer(self._audit).data
        except Audit.DoesNotExist:
            return False
