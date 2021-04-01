#########################################################
#   活动根异常
#       |
#       |__公共活动共有异常
#       |       |
#       |       |__初始化失败
#       |
#       |__晚查寝活动异常
#
#########################################################


class ActivityException(Exception):
    """活动根异常,所有活动的异常都应该至少从此异常继承"""


class ActivityPublicException(ActivityException):
    """所有活动的公共异常"""


class ActivityInitialization(ActivityPublicException):
    """活动初始化异常"""


class DormitoryEveningCheckException(ActivityException):
    """晚查寝活动根异常"""
