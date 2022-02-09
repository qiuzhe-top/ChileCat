'''
Author: 邹洋
Date: 2022-02-07 11:26:10
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-08 12:20:35
Description: 
'''
from django.contrib import admin

# Register your models here.

# @admin.register(StuInRoom)
# class StuInRoomAdmin(AjaxAdmin):
#     list_display = (
#         "id", "room","user", "user_name",'bed_position'
#     )
#     list_filter = ("room__floor__building__name","room__floor__name","room__name",)
#      # 增加自定义按钮
#     list_per_page = 20
#     search_fields = ("user__username","user__name")
#     actions = ('upload_file',)

#     def upload_file(self, request, queryset):
#         # 这里的upload 就是和params中配置的key一样
#         upload= request.FILES
        
#         print(upload)
#         return JsonResponse(data={
#                 'status': 'error',
#                 'msg': '请先选中数据！'
#             })


#     upload_file.short_description = '文件上传对话框'
#     upload_file.type = 'success'
#     upload_file.icon = 'el-icon-upload'
#     upload_file.enable = True

#     upload_file.layer = {
#         'params': [{
#             'type': 'file',
#             'key': 'upload',
#             'label': '文件'
#         },{
#             'type': 'number',
#             'key': 'money',
#             'label': '金额',
#             # 设置默认值
#             'value': 1000
#         }]
#     }
