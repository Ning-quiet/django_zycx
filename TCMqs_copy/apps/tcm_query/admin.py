from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from  .models import  TcmDetailInfomations,Banner,CheseHerbsShow,TcmPic
class TcmPicTabularInline(admin.TabularInline):
    model = TcmPic  # 多类的名字
    extra = 1
    fields = ('tcm_title','image')



class TcmDetailInfomationsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        # models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_display = ['tcm_title', 'scientific_name', 'show_alias', 'show_family_name', 'show_forum_on_tcm',
                    'show_channel_entry',"show_five_tastes",'show_toxicity_of','four_gas','show_medicinal',
                    'show_efficacy_function','show_efficacy_category', 'show_detail_desc',
                    'show_source','show_medicinal_part','medicinal_part_ca',
                    'banner','chese_herb_show','view_count','create_time']
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    # 要搜索的列的值
    search_fields = ['tcm_title']
    ordering = ('-create_time',)
    empty_value_display = ''
    readonly_fields =('view_count',)


    inlines = [TcmPicTabularInline]

class BannerAdmin(admin.ModelAdmin):
    list_display = ['tcm_title', 'tcm_banner','is_show','create_time']
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    # 要搜索的列的值
    search_fields = ['tcm_title']
    list_filter = ['tcm_title']


class  CheseHerbsShowAdmin(admin.ModelAdmin):
    list_display = ['tcm_title', 'tcm_show', 'is_show','create_time']
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    # 要搜索的列的值
    search_fields = ['tcm_title']

class TcmPicAdmin(admin.ModelAdmin):
    list_display = ['tcm_title', 'image','tcm_detail_info' ,'create_time']
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    # 要搜索的列的值
    search_fields = ['tcm_title']


admin.site.register(Banner, BannerAdmin)
admin.site.register(CheseHerbsShow,CheseHerbsShowAdmin)
admin.site.register(TcmPic,TcmPicAdmin)
admin.site.register(TcmDetailInfomations,TcmDetailInfomationsAdmin)





