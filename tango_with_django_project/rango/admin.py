from django.contrib import admin
from rango.models import Category,Page,UserProfile
# Register your models here.
# 添加这个类，定制管理界面

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


#注册 admin.site.register()
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(UserProfile)
