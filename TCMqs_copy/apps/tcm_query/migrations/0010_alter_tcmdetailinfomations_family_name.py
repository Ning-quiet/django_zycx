# Generated by Django 3.2.12 on 2022-05-16 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcm_query', '0009_alter_tcmdetailinfomations_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tcmdetailinfomations',
            name='family_name',
            field=models.TextField(blank=1, null=1, verbose_name='科名'),
        ),
    ]