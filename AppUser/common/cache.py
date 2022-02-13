'''
Author: 邹洋
Date: 2022-02-07 13:38:38
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 13:39:46
Description: 
'''

from AppUser.models import User
from cool import views

class UserSer(views.BaseSerializer):
    class Meta:
        model = User   # 模型名
        fields  = ['username'] 

# cache = InitCacheConnection().cache
# class UseCache():
#     '''
#     用户信息缓存

#     Args:
#         InitCacheConnection ([type]): 缓存基础类
#     '''
#     KEY = 'User'

#     def get_user_dict(user,dumps=True):
#         user_info = {}
#         groups = user.groups.all().values_list('name', flat=True)
#         permissions = user.user_permissions.all().values_list('codename', flat=True)
#         user_info['id'] = user.id
#         user_info['username'] = user.username
#         user_info['name'] = user.name
#         user_info['gender'] = user.gender
#         user_info['tel'] = user.tel
#         user_info['email'] = user.email
#         user_info['home_address'] = user.home_address
#         user_info['card_id'] = user.card_id
#         user_info['is_active'] = user.is_active
#         user_info['is_staff'] = user.is_staff
#         user_info['photo'] = user.photo
#         user_info['wx_openid'] = user.wx_openid
#         user_info['grade'] = None
#         user_info['groups'] = list(groups)
#         user_info['permissions'] = list(permissions)
#         if dumps:
#             return json.dumps(user_info)
#         else:
#             return user_info

#     def updata_user(self,user):
#         data = User.get_user_dict(user)
#         cache.hset(UseCache.KEY,user.username,data)

#     def init_data(self):
#         k = cache.keys(UseCache.KEY)
#         if len(k)==1:
#             return self
#         user_dict = {}
#         grade_dict = {}
#         try:
#             grade_info ,flg = self.qrpc('GradeManage',{'type':'get_grade_user_all'})   
#             for grade in grade_info:
#                 grade_dict[grade['username']] = grade['grade_id']
#         except:
#             pass
#         users = User.objects.all()
#         for user in users:
#             u = UseCache.get_user_dict(user,False)
#             try:
#                 u['grade'] = grade_dict[u['username']]
#             except:
#                 pass
#             user_dict[user.username] =  json.dumps(u)
        
#         cache.hmset(UseCache.KEY,user_dict)   
#         cache.expire(UseCache.KEY,60*60*24)

