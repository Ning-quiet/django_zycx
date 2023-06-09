# Generated by Django 3.2.12 on 2022-05-12 14:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0008_auto_20220512_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='tcmvideo',
            name='collected',
            field=models.ManyToManyField(blank=True, related_name='collected_videos', to=settings.AUTH_USER_MODEL, verbose_name='收藏的用户'),
        ),
        migrations.AddField(
            model_name='tcmvideo',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='liked_videos', to=settings.AUTH_USER_MODEL, verbose_name='喜欢的用户'),
        ),
    ]
