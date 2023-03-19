from django.contrib import admin
from  .models import  User

#更改 admin的title header 和名称
admin.site.site_header = '中药查询后台管理信息系统'
admin.site.site_title = '中药查询后台管理信息系统'
admin.site.index_title = "欢迎您登录,中药查询后台系统"

admin.site.register([User])
# Register your models here.
