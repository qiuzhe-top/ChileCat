class attendance_interface(object):
    '''考勤基础类'''

    def task_create(self):
        '''创建任务
        '''
        pass

    def task_delete(self):
        '''删除任务
        '''
        pass

    def task_update(self):
        '''修改任务
        '''
        pass

    def task_all(self):
        '''获取任务
        管理员获取自己创建或者管理的任务
        '''
        pass
    
    def add_admin(self):
        '''添加管理员
        一个考勤任务添加多个管理员，实现共同管理
        例如：在查寝任务上一个查寝任务有3栋楼需要检查，
        就可以分配多个管理员来查看或修改当前任务
        '''
        pass

    def delete_admin(self):
        '''删除管理员
        '''
        pass

    def task_status(self):
        '''任务状态 开启/关闭
        考勤任务一般在特点时间才执行，所以不在这个时间段就关闭任务
        例如：晚查寝只在每天晚上9:50左右
        '''
        pass
    
    def scheduling(self):
        '''排班
        对任务的人员安排，被排版的学生，登录工作平台
        可以有对应的任务显示
        '''
        pass

    def condition(self):
        '''查看考勤工作情况      
        '''

        '''查看晚查寝记录情况
        管理员在后台查看当前晚查寝被记录的名单
        '''

        '''
        查看卫生记录情况
        管理员在后台查看当前晚查寝被记录的名单
        '''

        '''查看晚自修记录情况
        管理员在后台查看晚自修情况
        显示各班点名不在情况、总体违纪记录情况
        需要按照时间筛选，因为当天是可以不看的
        但是在每周会进行一次销假需要查看
        '''
        pass

    def progress(self):
        '''查看考勤进度
        
        '''

        '''查看晚查寝进度
        管理员在后台查看晚查寝进度
        包括一栋楼检查进度、一层楼内房间检查进度、各个执行人是否确认任务完成
        '''
        '''查看卫生进度
        管理员在后台查看晚查寝进度
        包括一栋楼检查进度、一层楼内房间检查进度、各个执行人是否确认任务完成
        '''
        pass


    
    def undo_record(self):
        '''销假
        '''

        '''晚查寝销假
        针对当天会有晚归的同学，对其进行销假
        例如查寝结束时间为10点，而学生归寝时间为10.20
        这个时候就对其进行销假
        '''
        '''晚自修销假
        每周五对这一周的考勤记录进行销假，销假
        需要以学生提供的请假条为依据进行
        '''
        pass


    def out_data(self):
        '''数据导出
        '''

        '''晚查寝导出数据
        导出今天晚查寝结果
        '''

        '''卫生检查导出数据
        导出本次卫生检查结果
        '''

        '''晚自修导出数据
        导出本次检查结果
        '''

        '''导出本周任务情况'''

        pass
    

    
    def get_task_executor(self):
        '''执行人获取任务
        执行人获取今日的任务 包括 查寝、查卫生、晚自修
        '''
        pass
    

    def rule(self):
        '''获取规则
        '''

        '''查卫生规则
        获取卫生检查规则数据
        '''
        '''晚查寝规则
        获取晚查寝规则数据
        '''

        pass
    def student_information(self):
        '''获取学生信息
        
        通过学号获取学生信息
        在排班的时候用到
        在违规记录时用到
        应该属于另外模块的内容
        '''
        pass

    def submit(self):
        '''考勤提交
        '''
        '''晚查寝提交任务
        记录不在的学生进行提交
        '''
        '''晚自修提交违规情况
        晚自修对学生进行违规处理
        '''
        '''晚自修提交点名情况
        晚自修对学生进行点名处理
        '''
        '''晚自修提交违纪情况
        晚自修对学生进行违纪处理
        '''
        pass

    def executor_finish(self):
        '''执行人确认任务完成'''
        pass



class late_interface(attendance_interface):
    '''
    晚自修
    '''

    def get_class(self):
        '''晚自修-管理的班级
        执行人在手机上可以选择班级，这个班级数据来源于
        这次任务创建的时候绑定的班级
        '''
        pass

    def class_students(self):
        '''晚自修-班级内的学生
        选择班级后展示班级内学生列表，同时显示学生的2次点名情况
        '''
        pass


class knowing_interface(attendance_interface):
    '''
    晚查寝
    '''
    def storey(self):
        '''晚查寝-楼工作数据
        例如：晚查寝执行人进入楼层展示楼和楼下有那些层的数据
        '''
        pass

    def room(self):
        '''晚查寝-层工作数据
        例如：晚查寝执行人进入2楼展示2楼的房间数据
        '''
        pass

    def room_students(self):
        '''晚查寝-房间工作数据
        晚查寝执行人点击房间获取房间内学生的数据
        '''
        pass


class health_interface(knowing_interface):
    '''
    查卫生
    '''
    
    def storey(self):
        '''晚查寝-楼工作数据
        例如：查卫生执行人进入楼层展示楼和楼下有那些层的数据
        '''
        pass

    def room(self):
        '''晚查寝-层工作数据
        例如：查卫生执行人进入2楼展示2楼的房间数据
        '''
        pass

    def room_students(self):
        '''晚查寝-房间工作数据
        晚查寝执行人点击房间获取房间内学生的数据
        '''
        pass

class attendance_admin_interface(object):
    '''
    考勤系统管理员
    汇总本学院的 查寝 晚自修 模块
    对其进行销假 导出
    '''
    def out(self):
        pass