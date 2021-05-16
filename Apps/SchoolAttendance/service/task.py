
from .knowing import knowing
from .health import health
from .late import late
# from Apps.SchoolAttendance.service.late import late

'''
任务公共类
'''

task_factory = {
    '0': knowing,
    '1': health,
    '2': late
}


class task(object):

    def add_admin(self):
        '''添加管理员
        '''
        pass

    def switch(self):
        '''任务开启
        '''
        console_code = self._activity.console_code
        console_code = not console_code
        if console_code:
            self.initialization()
        self._activity.console_code = console_code
        self._activity.save()
        return console_code

    # def task_create(self):
