# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0005_auto_20150718_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='s_commit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('s_time', models.DateTimeField(verbose_name='Время сдачи отчета')),
                ('s_prim', models.TextField(verbose_name='Примечание')),
            ],
            options={
                'verbose_name_plural': 'Сдача отчета',
                'verbose_name': 'Сдача отчета',
            },
        ),
        migrations.AlterField(
            model_name='s_fault',
            name='f_staff',
            field=models.ForeignKey(verbose_name='Пользователь', to='otchet.CustomUser'),
        ),
        migrations.AddField(
            model_name='s_commit',
            name='s_fault_commit',
            field=models.ForeignKey(verbose_name='Последний коммит (сбои)', to='otchet.s_fault'),
        ),
        migrations.AddField(
            model_name='s_commit',
            name='s_lift_commit',
            field=models.ForeignKey(verbose_name='Последний коммит (лифты)', to='otchet.s_drop_lift'),
        ),
        migrations.AddField(
            model_name='s_commit',
            name='s_staff_commit',
            field=models.ForeignKey(to='otchet.CustomUser'),
        ),
    ]
