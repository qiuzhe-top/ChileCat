"""定义异常文件"""


class LoginExcept(Exception):
    """登录异常"""


class VxLoginException(LoginExcept):
    """微信登录失败异常"""


class VxAuthException(VxLoginException):
    """获取微信openid失败"""


class VxBindException(VxLoginException):
    """微信未绑定"""


class WebLoginException(LoginExcept):
    """网页登录异常"""


class ParamException(Exception):
    """参数缺失"""
