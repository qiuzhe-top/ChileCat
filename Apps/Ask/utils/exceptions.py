"""请假条,审核相关的异常"""


class AskAndAuditException(Exception):
    """请假和审批的基异常"""


class AuditException(AskAndAuditException):
    """审批异常"""


class AuthAuditException(AuditException):
    """审批权限异常"""


class NextAuditException(AuditException):
    """没有下一个审批老师"""


class AlreadyAuditException(AuditException):
    """对已经完成的请假条进行审批"""


class AskException(AskAndAuditException):
    """请假条异常"""


class AskAddTimeException(AskException):
    """续假异常"""
