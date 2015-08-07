# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, to=settings.AUTH_USER_MODEL, parent_link=True)),
                ('birthday', models.DateField(null=True, blank=True, verbose_name='birthday')),
                ('p_num', models.SmallIntegerField(verbose_name='Табельный номер')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
                ('telephone', models.CharField(max_length=15, blank=True, verbose_name='Телефон')),
                ('fired', models.BooleanField(verbose_name='Уволен', default=False)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='s_group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('group_name', models.CharField(max_length=150, verbose_name='Название группы')),
            ],
            options={
                'verbose_name_plural': 'Группы',
                'verbose_name': 'Группа',
            },
        ),
        migrations.CreateModel(
            name='s_office',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('office_name', models.CharField(max_length=50, verbose_name='Должность')),
                ('group', models.ManyToManyField(to='otchet.s_group', verbose_name='Группа')),
            ],
            options={
                'verbose_name_plural': 'Должности',
                'verbose_name': 'Должность',
            },
        ),
        migrations.CreateModel(
            name='s_timetable',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('smena', models.CharField(max_length=10, verbose_name='Смена')),
            ],
            options={
                'verbose_name_plural': 'График работы',
                'verbose_name': 'График работы',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='group',
            field=models.ForeignKey(to='otchet.s_group', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='office',
            field=models.ForeignKey(to='otchet.s_office', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='timetable',
            field=models.ForeignKey(to='otchet.s_timetable', verbose_name='График работы'),
        ),
    ]
