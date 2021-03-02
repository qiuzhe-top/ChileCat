"""exceptions"""


class LifeException(Exception):
    """本模块根异常"""


class ActivityException(LifeException):
    """活动相关的异常"""


class TimeActivityException(ActivityException):
    """活动时间异常"""


class VerificationCodeException(ActivityException):
    """验证码相关异常"""


class VerifyVerificationCodeException(VerificationCodeException):
    """确认验证码异常"""


class TimeVerificationCodeException(VerificationCodeException):
    """验证码时间异常"""


class DormitoryException(LifeException):
    """寝室相关异常"""


class RoomParamException(DormitoryException):
    """房间参数异常"""
