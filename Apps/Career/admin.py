'''
admin.py
'''
from django.contrib import admin
from .models import Career,Primitives,TypePar,TypeChild

@admin.register(Career)
class CareerTeleAdmin(admin.ModelAdmin):
    '''
    职业文章
    '''
    list_display = ("id","title")
@admin.register(Primitives)
class PrimitivesTeleAdmin(admin.ModelAdmin):
    '''
    作品(?)
    '''
    list_display = ("id","title")
@admin.register(TypePar)
class TypeParTeleAdmin(admin.ModelAdmin):
    '''
    分类父表
    '''
    list_display = ("id","title","par_id")
@admin.register(TypeChild)
class TypeChildTeleAdmin(admin.ModelAdmin):
    '''
    分类字表
    '''
    list_display = ("id","title","par_id")
