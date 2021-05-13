"""exceptions"""


class LifeException(Exception):
    """本模块根异常"""


class DormitoryException(LifeException):
    """寝室相关异常"""


class RoomParamException(DormitoryException):
    """房间参数异常"""
