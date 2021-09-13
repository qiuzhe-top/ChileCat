<!--
 * @Author: 邹洋
 * @Date: 2021-07-04 13:27:27
 * @Email: 2810201146@qq.com
 * @LastEditors:  
 * @LastEditTime: 2021-09-13 21:17:55
 * @Description: 
-->
## 分配考勤管理员
分配权限实现后台登陆，和相对应考勤页面的进入
 - 设置用户 勾选 《工作人员状态》 确保能够登录后台
 - 用户先添加到 attendance_admin 组
 - 根据情况添加到 查寝 晚自修 卫生 等的分组
 - 使用用户创建任务
 - 把任务相关的管理员进行绑定.



pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
npm config set registry https://registry.npm.taobao.org
pip install -r requirement.txt


python manage.py makemigrations User
python manage.py makemigrations SchoolInformation
python manage.py makemigrations SchoolAttendance

python manage.py migrate

python manage.py createsuperuser

qiuzhe
zhou24272592

python manage.py test Apps.SchoolAttendance.tests.


# 智慧彩云
### V 1.1.0
- 继承User拷贝UserAdmin完成注册，大部分代码进行替换但没有测试
- 完成自定义User移植
- 优化学生导入
- 修改默认密码为123456
- 上传学生信息时要求传递分院CodenName
- 修复权益部按照分院进行违纪搜索
- 删除任务时任务记录关于用户的地方采用默认值
- 权益部汇总统计 晚自修旷课分数修改 都不在扣2，有一个不在扣3
- 考勤规则初始化优化 实现3级规则创建
### V 1.0.1
- 去除重置查寝任务状态多余的重置房间的循环
- 修正SubmitKnowing 寝室考勤逻辑
  - 优化不能第二次提交的规则
- 修正撤销学生不生效问题 改为具体考勤类里面实现
### V 1.0.1
- 实现对楼层和房间按顺序排序
- 修正前端出现自定义规则这个分类
### V 1.0 
- 完成基本功能
<!-- 主版本号.子版本号[.修正版本号[.编译版本号]] -->
1、GUN风格：

（1）产品初版时，版本号可以为0.1或0.1.0，也可以为1.0或1.0.0；

（2）当产品进行了局部修改或bug修正时，主版本号和子版本号都不变，修正版本号+1；

（3）当产品在原有的基础上增加了部分功能时，主版本号不变，子版本号+1，修正版本号复位为0；

（4）当产品进行了重大修改或局部修正累计较多，而导致产品整体发生全局变化的，主版本号+1；

（5）编译版本号，一般是编译器在编译过程中自动生成的，我们只定义其格式，并不进行人为控制；