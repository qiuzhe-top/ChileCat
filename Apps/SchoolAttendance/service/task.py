
from .. import models

# from Apps.SchoolAttendance.service.late import late
from . import knowing, health, late
'''
任务公共类
'''
task_factory = {
    '0': knowing.Knowing,
    '1': health.Health,
    '2': late.Late
}


class TaskManage(object):

    def create_task(self,task,ids):

        task_factory[task.types](task).task_create(ids)
        
    def add_admin(self):
        '''添加管理员
        '''
        pass

    def switch(self,id):
        '''任务开启
        '''
        task = models.Task.objects.get(id=id)
        task.is_open = not task.is_open
        flg = task.is_open
        task.save()
        return flg

    # def task_create(self):
