from django.contrib import admin
from Manage.models import Primitives,TypePar,TypeChild

# Register your models here.

@admin.register(Primitives)
class primitivesTeleAdmin(admin.ModelAdmin):
    list_display = ("id","title")
@admin.register(TypePar)
class TypeParTeleAdmin(admin.ModelAdmin):
    list_display = ("id","title","par_id")
@admin.register(TypeChild)
class TypeChildTeleAdmin(admin.ModelAdmin):
    list_display = ("id","title","par_id")
