# Generated by Django 2.0.4 on 2018-07-12 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AssocMgnt', '0004_auto_20180711_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(default='A0000', max_length=16, verbose_name='学号/员工号'),
            preserve_default=False,
        ),
    ]