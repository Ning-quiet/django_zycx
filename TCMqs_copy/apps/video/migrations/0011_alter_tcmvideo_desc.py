# Generated by Django 3.2.12 on 2022-05-17 06:13

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0010_auto_20220512_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tcmvideo',
            name='desc',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='描述'),
        ),
    ]
