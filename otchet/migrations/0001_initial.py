# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, to=settings.AUTH_USER_MODEL, serialize=False, parent_link=True, primary_key=True)),
                ('birthday', models.DateField(blank=True, verbose_name='birthday', null=True)),
                ('p_num', models.SmallIntegerField(blank=True, verbose_name='Табельный номер', null=True)),
                ('patronymic', models.CharField(blank=True, max_length=50, verbose_name='Отчество', null=True)),
                ('telephone', models.CharField(blank=True, max_length=15, verbose_name='Телефон', null=True)),
                ('fired', models.BooleanField(default=False, verbose_name='Уволен')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='s_commit',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('s_time', models.DateTimeField(verbose_name='Время сдачи отчета')),
                ('s_prim', models.TextField(blank='True', verbose_name='Примечание', null='True')),
            ],
            options={
                'verbose_name': 'Сдача отчета',
                'verbose_name_plural': 'Сдача отчета',
            },
        ),
        migrations.CreateModel(
            name='s_drop_lift',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('stop_lift', models.DateTimeField(verbose_name='Время остановки')),
                ('start_lift', models.DateTimeField(blank=True, verbose_name='Время запуска')),
                ('description', models.CharField(blank=True, max_length=50, verbose_name='Описание')),
                ('consequences', models.BooleanField(verbose_name='Без последствий')),
            ],
            options={
                'ordering': ['stop_lift'],
                'verbose_name': 'Остановка лифта (эскалатора)',
                'verbose_name_plural': 'Остановка лифтов (эскалаторов)/падения',
            },
        ),
        migrations.CreateModel(
            name='s_fault',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('fault_time', models.DateTimeField(verbose_name='Время')),
                ('description', models.CharField(max_length=500, verbose_name='Описание')),
                ('correction', models.BooleanField(default=False, verbose_name='Устранено')),
                ('f_staff', models.ForeignKey(to='otchet.CustomUser', verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['fault_time'],
                'verbose_name': 'Происшествие',
                'verbose_name_plural': 'Происшествия',
            },
        ),
        migrations.CreateModel(
            name='s_fault_lift',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('type_fault', models.CharField(max_length=50, verbose_name='Причины остановки')),
            ],
            options={
                'verbose_name': 'Причина остановки',
                'verbose_name_plural': 'Причины остановки',
            },
        ),
        migrations.CreateModel(
            name='s_group',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=150, verbose_name='Название группы')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.CreateModel(
            name='s_lift',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('ser_num', models.SmallIntegerField(verbose_name='Номер')),
                ('l_type', models.CharField(max_length=1, verbose_name='Тип', choices=[('Л', 'Лифт'), ('Э', 'Эскалатор')])),
                ('terminal', models.CharField(max_length=1, verbose_name='Терминал', choices=[('A', 'Терминал A'), ('B', 'Терминал B')])),
                ('location', models.CharField(max_length=50, verbose_name='Месторасположение, направление, этаж')),
            ],
            options={
                'ordering': ['ser_num'],
                'verbose_name': 'Лифт/Эскалатор',
                'verbose_name_plural': 'Лифты/Эскалаторы',
            },
        ),
        migrations.CreateModel(
            name='s_objects',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
            ],
            options={
                'verbose_name': 'Объект',
                'verbose_name_plural': 'Объекты',
            },
        ),
        migrations.CreateModel(
            name='s_office',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('office_name', models.CharField(max_length=50, verbose_name='Должность')),
                ('group', models.ManyToManyField(to='otchet.s_group', verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='s_system',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('system_name', models.CharField(max_length=50, verbose_name='Название системы')),
                ('group', models.ForeignKey(to='otchet.s_group', verbose_name='Ответственная группа')),
            ],
            options={
                'ordering': ['system_name'],
                'verbose_name': 'Система',
                'verbose_name_plural': 'Системы',
            },
        ),
        migrations.CreateModel(
            name='s_timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('smena', models.CharField(max_length=10, verbose_name='Смена')),
            ],
            options={
                'verbose_name': 'График работы',
                'verbose_name_plural': 'График работы',
            },
        ),
        migrations.AddField(
            model_name='s_objects',
            name='system',
            field=models.ManyToManyField(blank=True, to='otchet.s_system', verbose_name='Системы'),
        ),
        migrations.AddField(
            model_name='s_fault',
            name='f_system',
            field=models.ForeignKey(to='otchet.s_system', verbose_name='Система'),
        ),
        migrations.AddField(
            model_name='s_fault',
            name='s_object',
            field=models.ForeignKey(to='otchet.s_objects', verbose_name='Объект'),
        ),
        migrations.AddField(
            model_name='s_drop_lift',
            name='fault',
            field=models.ForeignKey(to='otchet.s_fault_lift', verbose_name='Тип'),
        ),
        migrations.AddField(
            model_name='s_drop_lift',
            name='lift_name',
            field=models.ForeignKey(to='otchet.s_lift', verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='s_commit',
            name='s_fault_commit',
            field=models.ForeignKey(to='otchet.s_fault', verbose_name='Последний коммит (сбои)'),
        ),
        migrations.AddField(
            model_name='s_commit',
            name='s_lift_commit',
            field=models.ForeignKey(to='otchet.s_drop_lift', verbose_name='Последний коммит (лифты)'),
        ),
        migrations.AddField(
            model_name='s_commit',
            name='s_staff_commit',
            field=models.ForeignKey(to='otchet.CustomUser'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='group',
            field=models.ForeignKey(blank=True, null=True, to='otchet.s_group', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='office',
            field=models.ForeignKey(blank=True, null=True, to='otchet.s_office', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='timetable',
            field=models.ForeignKey(blank=True, null=True, to='otchet.s_timetable', verbose_name='График работы'),
        ),
    ]
