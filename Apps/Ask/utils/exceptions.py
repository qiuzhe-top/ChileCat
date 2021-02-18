"""请假条,审核相关的异常"""


class AuditException(Exception):
    """审批异常"""


class AuthAuditException(AuditException):
    """审批权限异常"""


class NextAuditException(AuditException):
    """没有下一个审批老师"""
