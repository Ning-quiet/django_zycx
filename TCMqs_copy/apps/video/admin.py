from django.contrib import admin
from .models import *
class VideoTabularInline(admin.TabularInline):
    model = TcmVideo   # 多类的名字
    extra = 1
    fields = ('title','desc','file','cover','status')

class TcmVideoClassificationAdmin(admin.ModelAdmin):
    # 指定后台网页要显示的字段
    list_display = ["title", "status","create_time"]
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    inlines = [VideoTabularInline]
    # 要搜索的列的值
    search_fields = ['title']
    # list_filter = ['title']

class TcmvideoAdmin(admin.ModelAdmin):
    list_display = ['title','show_desc','file','cover','status','classification','create_time']
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    # 要搜索的列的值
    search_fields = ['title','cover']
admin.site.register(TcmVideo,TcmvideoAdmin)
admin.site.register(TcmVideoClassification,TcmVideoClassificationAdmin)

