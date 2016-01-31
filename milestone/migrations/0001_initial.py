# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MilestoneUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('firstName', models.CharField(max_length=50, blank=True, verbose_name='Имя', null=True)),
                ('patroName', models.CharField(max_length=50, blank=True, verbose_name='Отчество', null=True)),
                ('lastName', models.CharField(max_length=50, blank=True, verbose_name='Фамилия', null=True)),
                ('loginName', models.CharField(max_length=50, verbose_name='Логин')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='MilLogin',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('lQuant', models.IntegerField()),
                ('lDate', models.DateField()),
            ],
            options={
                'verbose_name': 'Milestone Login',
                'verbose_name_plural': 'Milestone Login',
            },
        ),
        migrations.CreateModel(
            name='sysSec',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('ipAddress', models.GenericIPAddressField()),
                ('sysName', models.CharField(max_length=50, blank=True, verbose_name='Название', null=True)),
                ('description', models.CharField(max_length=50, blank=True, verbose_name='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Система',
                'verbose_name_plural': 'Системы',
            },
        ),
        migrations.AddField(
            model_name='millogin',
            name='lIP',
            field=models.ManyToManyField(to='milestone.sysSec'),
        ),
        migrations.AddField(
            model_name='millogin',
            name='lUser',
            field=models.ForeignKey(to='milestone.MilestoneUser'),
        ),
    ]
