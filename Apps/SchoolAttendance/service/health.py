from . import task
from .. import models
from .knowing import Knowing
'''
寝室卫生
'''


class Health(Knowing):

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

    def submit(self,data,worker_user):
        '''考勤提交
        '''
        print(data)

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
