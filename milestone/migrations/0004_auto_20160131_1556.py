# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0003_auto_20160131_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syssec',
            name='ipAddress',
            field=models.GenericIPAddressField(unique=True),
        ),
        migrations.AlterField(
            model_name='syssec',
            name='milUser',
            field=models.ForeignKey(verbose_name='Пользователь Milestone', null=True, to='milestone.MilestoneUser', blank=True),
        ),
    ]
