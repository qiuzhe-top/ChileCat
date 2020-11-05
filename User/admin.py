from django.contrib import admin
from .models import *

@admin.register(User)
class UserTeleAdmin(admin.ModelAdmin):
    list_display = ("id","user_name","pass_word")

@admin.register(Token)
class TokenTeleAdmin(admin.ModelAdmin):
    list_display = ("id","token","wx_openid")