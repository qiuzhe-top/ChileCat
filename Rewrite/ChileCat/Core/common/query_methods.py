
from django.db.models import Aggregate, CharField, F


class Msum(Aggregate):
    # Supports SUM(ALL field).
    function = 'SUM'
    template = '%(function)s(%(all_values)s%(expressions)s)'
    allow_distinct = False

    def __init__(self, expression, all_values=False, **extra):
        # print(self, expression, all_values, **extra)
        super().__init__(expression, all_values='ALL ' if all_values else '', **extra)
        # return "123"
# 自定义聚合函数的名字
class Concat(Aggregate):  # 写一个类继承Aggregate，
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            arg_joiner="-",
            **extra
        )