# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-27 08:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradingApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='gtime',
            field=models.DateTimeField(auto_now=True, verbose_name='添加时间'),
        ),
    ]
