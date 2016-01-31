# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0002_auto_20160130_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='syssec',
            name='milUser',
            field=models.ForeignKey(to='milestone.MilestoneUser', null=True, verbose_name='Пользователь', blank=True),
        ),
        migrations.AlterField(
            model_name='millogin',
            name='lDate',
            field=models.DateField(default=datetime.date(2016, 1, 30)),
        ),
    ]
