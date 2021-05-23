
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

    def get_task_obj(self,id):
        return models.Task.objects.get(id=int(id))

    def create_task(self,task,ids):
        '''创建任务
        '''
        task_factory[task.types](task).task_create(ids)
        
    def add_admin(self):
        '''添加管理员
        '''
        pass

    def switch(self,id):
        '''任务开启
        '''
        task = self.get_task_obj(id)
        task.is_open = not task.is_open
        flg = task.is_open
        task.save()
        return flg

    def clear_task(self,id):
        '''清除任务状态
        '''
        task = self.get_task_obj(id)
        task_factory[task.types](task).clear_task()
    # def task_create(self):

    def scheduling(self,id,roster):
        '''保存班表
        '''
        task = self.get_task_obj(id)
        task_factory[task.types](task).scheduling(roster)
        pass

    def task_roomInfo(self,id,type,user):
        '''获取任务数据
        '''
        task = self.get_task_obj(id)
        if not models.TaskPlayer.objects.filter(task=task,user=user).exists():
            return ''
        if type == 0:
            return task_factory[task.types](task).storey()
        elif type == 1:
            return  task_factory[task.types](task).room()
        elif type == 2:
            return  task_factory[task.types](task).room_students()


