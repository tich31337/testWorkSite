# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='group',
            field=models.ForeignKey(null=True, to='otchet.s_group', verbose_name='Группа', blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='office',
            field=models.ForeignKey(null=True, to='otchet.s_office', verbose_name='Должность', blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='p_num',
            field=models.SmallIntegerField(verbose_name='Табельный номер', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='patronymic',
            field=models.CharField(verbose_name='Отчество', max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='telephone',
            field=models.CharField(verbose_name='Телефон', max_length=15, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='timetable',
            field=models.ForeignKey(null=True, to='otchet.s_timetable', verbose_name='График работы', blank=True),
        ),
    ]
