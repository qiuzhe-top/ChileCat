<!--
 * @Author: 邹洋
 * @Date: 2021-07-04 13:27:27
 * @Email: 2810201146@qq.com
 * @LastEditors:  
 * @LastEditTime: 2021-07-14 15:20:56
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