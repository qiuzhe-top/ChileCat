from . import task
from .. import models
'''
寝室卫生
'''


class health(object):

    def __init__(self, id):
        if id > 0:
            self.obj = models.Task.objects.get(id=id)
            self.user = self.obj.user

    def task_create(self, user, types, ids):
        '''创建任务
        '''

        dic = {
            'user': user,
            'is_open': True,
            'types': types,
            'college': user.studentinfo.grade.college,
        }
        task = models.Task.objects.create(**dic)
        task.buildings.set(ids)
        return True

    def add_admin(self):
        '''添加管理员
        '''
        pass

    def switch(self):
        '''任务开启
        '''
        pass

    def scheduling(self):
        '''排班
        '''
        pass

    def condition(self):
        '''查看考勤工作情况      
        '''
        pass

    def progress(self):
        '''查看考勤进度
        '''
        pass

    def undo_record(self):
        '''销假
        '''
        pass

    def out_data(self):
        '''数据导出
        '''
        pass

    def get_task(self):
        '''执行人获取任务
        执行人获取今日的任务 包括 查寝、查卫生、晚自修
        '''
        pass

    def rule(self):
        '''获取规则
        '''
        pass

    def student_information(self):
        '''获取学生信息
        '''
        pass

    def submit(self):
        '''考勤提交
        '''
        pass

    def executor_finish(self):
        '''执行人确认任务完成'''
        pass

    def storey(self):
        '''晚查寝-楼工作数据
        '''
        pass

    def room(self):
        '''晚查寝-层工作数据
        '''
        pass

    def room_students(self):
        '''晚查寝-房间工作数据
        '''
        pass
