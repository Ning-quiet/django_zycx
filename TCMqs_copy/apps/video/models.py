from django.db import models
from  dbs.base_model import BaseModel
#ClassificationTraditionalChineseMedicine(TCM)
from  TCMqs import  settings
from django.db import models
from tinymce.models import HTMLField

class VideoQuerySet(models.query.QuerySet):

    def get_recommend_list(self):
        return self.filter(status=1).order_by('-view_count')[:5]

class TcmVideoClassification(BaseModel,models.Model):
    STATUS_CHOICES = (
        ('1', '启用'),
        ('0', '不启用'),
    )
    title = models.CharField(max_length=100,blank=True, null=True,verbose_name='中药类别名称')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True, verbose_name='状态',default=1)
    def __str__(self):
        return  self.title
    class Meta:
        db_table = "tcm_video_classification"
        verbose_name = '中药视频类别'
        verbose_name_plural = verbose_name


class TcmVideo(BaseModel,models.Model):
    STATUS_CHOICES = (
        ('1', '发布中'),
        ('0', '未发布'),
    )
    def __str__(self):
        return self.title
    title = models.CharField(max_length=100,blank=True, null=True,verbose_name='视频名称')

    def show_desc(self):
        if len(str(self.desc)) > 10:  # 字数自己设置
            return '{}……'.format(str(self.desc)[0:10])  # 超出部分以省略号代替。
        else:
            return self.desc

    show_desc.short_description = "描述"
    desc = models.TextField(blank=True, null=True,verbose_name='描述')
    classification = models.ForeignKey(TcmVideoClassification, on_delete=models.DO_NOTHING, null=True,verbose_name='类别')
    file = models.FileField(max_length=255,verbose_name='视频',upload_to='video')
    cover = models.ImageField(upload_to='cover',blank=True, null=True,verbose_name='封面')
    status = models.CharField(max_length=1 ,choices=STATUS_CHOICES, blank=True, null=True,verbose_name='状态',default=0)
    view_count = models.IntegerField(default=0, blank=True,verbose_name='观看次数')


    objects = VideoQuerySet.as_manager()

    class Meta:
        db_table = "tcm_video"
        verbose_name = '中药视频'
        verbose_name_plural = verbose_name


    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])


# Create your models here.
