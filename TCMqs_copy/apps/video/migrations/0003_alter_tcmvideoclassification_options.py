# Generated by Django 3.2.12 on 2022-04-30 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_alter_tcmvideoclassification_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tcmvideoclassification',
            options={'verbose_name': '中药视频类别', 'verbose_name_plural': '中药视频类别'},
        ),
    ]
