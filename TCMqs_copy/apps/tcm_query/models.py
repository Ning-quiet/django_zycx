from django.db import models
from dbs.base_model import  BaseModel
from tinymce.models import  HTMLField



class TcmDetailInfoQuerySet(models.query.QuerySet):

    #查询凉性
    def get_liangxing(self):
        return  self.filter(four_gas__contains
='凉')
    #查询热性
    def get_rexing(self):
        return  self.filter(four_gas__contains
='热')
    #查询温性
    def get_wenxing(self):
        return  self.filter(four_gas__contains
='温')
    #查询寒性
    def get_hanxing(self):
        return  self.filter(four_gas__contains
='寒')
    #查询平性
    def get_pingxing(self):
        return  self.filter(four_gas__contains
='平')
    def get_all(self):
        return  self.all().exclude(medicinal_part_ca='').order_by('medicinal_part_ca')

    def get_recommend_list(self):
        return self.all().order_by('-view_count')[:4]
    def get_yaoming(self):
        return  self.all()

    def get_gongxiao(self):
        return  self.all().order_by('efficacy_category')
    def get_guijing(self):
        return self.all().order_by('channel_entry')
    





# banner 首页轮播图
class Banner(BaseModel,models.Model):
     tcm_title=models.CharField(verbose_name='中药名称',max_length=128,blank=1,null=1)
     # brief_desc=models.CharField(verbose_name="简答描述",max_length=128,blank=1,null=1)
     tcm_banner=models.ImageField(upload_to="tcm_banner",verbose_name='轮播图',blank=True, null=True)
     STATUS_CHOICES = (
         ('1', '展示'),
         ('0', '不展示'),
     )
     is_show = models.CharField(verbose_name="是否展示", max_length=4, blank=1, null=1, choices=STATUS_CHOICES, default=0)

     class Meta:
        db_table = "tcm_banner"
        verbose_name="首页轮播图"
        verbose_name_plural=verbose_name
     def __str__(self):
         return   self.tcm_title


class CheseHerbsShow(BaseModel, models.Model):
    STATUS_CHOICES = (
        ('1', '展示'),
        ('0', '不展示'),
    )
    tcm_title = models.CharField(verbose_name='中药名称', max_length=255, null=1)
    tcm_show = models.ImageField(upload_to="tcm_banner", verbose_name='展示图', blank=True, null=True)
    is_show = models.CharField(verbose_name="是否展示", max_length=4, blank=1, null=1, choices=STATUS_CHOICES,
                               default=0)

    class Meta:
        db_table = "tcm_herb_show"
        verbose_name = "首页展示"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tcm_title


#详细中药介绍
class TcmDetailInfomations(BaseModel,models.Model):
    def desc_fields_show(self):
        if len(self.detail_desc) > 80:  # 字数自己设置
            return '{}……'.format(self.detail_desc[0:80])  # 超出部分以省略号代替。
        else:
            return  self.detail_desc
    tcm_title = models.CharField(verbose_name='中药名称', max_length=128, blank=1, null=1,db_index=1)
    scientific_name=models.CharField(verbose_name='学名',max_length=128,blank=1,null=1)
    alias=models.CharField(verbose_name='别名',max_length=255,blank=1,null=1)
    channel_entry = models.CharField(verbose_name='归经', max_length=255, blank=1, null=1)
    five_tastes = models.CharField(verbose_name="五味", max_length=255, blank=1, null=1)  # 药味
    toxicity_of = models.CharField(verbose_name="毒性", max_length=255, blank=1, null=1)
    forum_on_tcm = models.CharField(verbose_name="升降浮沉", max_length=255, blank=1, null=1)
    four_gas = models.CharField(verbose_name="四气", max_length=125, blank=1, null=1)  # 寒热
    medicinal = models.TextField(verbose_name='药性', max_length=255, blank=1, null=1)

    STATUS_CHOICES = (
        ('0', '全草'),
        ('1', '叶类'),
        ("2", '花'),
        ('3', '果实、种子'),
        ('4', '根、根茎'),
        ('5', '树皮、根皮'),

    )
    medicinal_part_ca=models.CharField(choices=STATUS_CHOICES,verbose_name="药用部位类别",blank=1,null=1,max_length=20)

    def show_alias(self):
        if len(str(self.alias)) > 10:  # 字数自己设置
            return '{}……'.format(str(self.alias)[0:10])  # 超出部分以省略号代替。
        else:
            return self.alias
    show_alias.short_description = "别名"
    family_name=models.TextField(verbose_name='药用部位',blank=1,null=1)

    def show_family_name(self):
        if len(str(self.family_name)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.family_name)[0:20])  # 超出部分以省略号代替。
        else:
            return self.family_name

    show_family_name.short_description = "药用部位"
    detail_desc=HTMLField(verbose_name="详细介绍",blank=1,null=1)
    def show_detail_desc(self):
        if len(str(self.detail_desc)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.detail_desc)[0:20])  # 超出部分以省略号代替。
        else:
            return  self.detail_desc
    show_detail_desc.short_description = "详细介绍"

    efficacy_function=models.TextField(verbose_name="功效作用",blank=1,null=1)
    def  show_efficacy_function(self):
        if len(str(self.efficacy_function)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.efficacy_function)[0:20])  # 超出部分以省略号代替。
        else:
            return self.efficacy_function
    show_efficacy_function.short_description='功效作用'

    efficacy_category=models.TextField(verbose_name="功效类别",max_length=255,blank=1,null=1)
    def show_efficacy_category(self):
        if len(str(self.efficacy_category)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.efficacy_category)[0:20])  # 超出部分以省略号代替。
        else:
            return self.efficacy_category

    show_efficacy_category.short_description = '功效类别'


    def show_forum_on_tcm(self):
        if len(str(self.forum_on_tcm)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.forum_on_tcm)[0:20])  # 超出部分以省略号代替。
        else:
            return self.forum_on_tcm
    show_forum_on_tcm.short_description = '升降浮沉'
    source=models.TextField(verbose_name="来源",max_length=255,blank=1,null=1)
    def  show_channel_entry(self):
        if len(str(self.channel_entry)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.channel_entry)[0:20])  # 超出部分以省略号代替。
        else:
            return self.channel_entry
    show_channel_entry.short_description='归经'
    def show_five_tastes(self):
        if len(str(self.five_tastes)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.five_tastes)[0:20])  # 超出部分以省略号代替。
        else:
            return self.five_tastes
    show_five_tastes.short_description='五味'
    def show_toxicity_of(self):
        if len(str(self.toxicity_of)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.toxicity_of)[0:20])  # 超出部分以省略号代替。
        else:
            return self.toxicity_of
    show_toxicity_of.short_description="毒性"


    def show_source(self):
        if len(str(self.source)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.source)[0:20])  # 超出部分以省略号代替。
        else:
            return self.source
    show_source.short_description = '来源'

    def show_medicinal(self):
        if len(str(self.medicinal)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.medicinal)[0:20])  # 超出部分以省略号代替。
        else:
            return self.medicinal
    show_medicinal.short_description="药性"
    medicinal_part=models.TextField(verbose_name="药物性状",blank=1,null=1)

    def show_medicinal_part(self):
        if len(str(self.medicinal_part)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.medicinal_part)[0:20])  # 超出部分以省略号代替。
        else:
            return self.medicinal_part
    show_medicinal_part.short_description='药物性状'
    view_count = models.IntegerField(default=0, blank=True,verbose_name='浏览次数')
    banner=models.OneToOneField(Banner,verbose_name="轮播图",null=1,on_delete=models.DO_NOTHING,blank=1)
    chese_herb_show = models.OneToOneField(CheseHerbsShow, verbose_name="展示图", null=1, on_delete=models.DO_NOTHING,
                                      blank=1)
    def __str__(self):
        return  self.tcm_title


    class Meta:
        db_table = "tcm_detail_info"
        verbose_name = "详细中药介绍"
        verbose_name_plural = verbose_name
    objects=TcmDetailInfoQuerySet.as_manager()

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

#中药图片类
class TcmPic(BaseModel,models.Model):
    tcm_title=models.CharField(verbose_name='图片名称',max_length=255,blank=1,null=1)
    image=models.ImageField(verbose_name="中药图片",upload_to="tcm_pic")
    tcm_detail_info=models.ForeignKey(TcmDetailInfomations,verbose_name='详细中药信息',null=1,on_delete=models.CASCADE)
    class Meta:
        db_table = "tcm_pic"
        verbose_name = "中药图片"
        verbose_name_plural = verbose_name
    def __str__(self):
        return  self.tcm_title




