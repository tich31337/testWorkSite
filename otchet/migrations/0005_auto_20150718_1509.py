# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('otchet', '0004_customuser_birthday'),
    ]

    operations = [
        migrations.CreateModel(
            name='s_drop_lift',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('stop_lift', models.DateTimeField(verbose_name='Время остановки')),
                ('start_lift', models.DateTimeField(blank=True, verbose_name='Время запуска')),
                ('description', models.CharField(blank=True, max_length=50, verbose_name='Описание')),
                ('consequences', models.BooleanField(verbose_name='Без последствий')),
            ],
            options={
                'verbose_name': 'Остановка лифта (эскалатора)',
                'verbose_name_plural': 'Остановка лифтов (эскалаторов)/падения',
                'ordering': ['stop_lift'],
            },
        ),
        migrations.CreateModel(
            name='s_fault',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('fault_time', models.DateTimeField(verbose_name='Время')),
                ('description', models.CharField(verbose_name='Описание', max_length=500)),
                ('correction', models.BooleanField(default=False, verbose_name='Устранено')),
                ('f_staff', models.ForeignKey(verbose_name='Пользователь', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Происшествие',
                'verbose_name_plural': 'Происшествия',
                'ordering': ['fault_time'],
            },
        ),
        migrations.CreateModel(
            name='s_fault_lift',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('type_fault', models.CharField(verbose_name='Причины остановки', max_length=50)),
            ],
            options={
                'verbose_name': 'Причина остановки',
                'verbose_name_plural': 'Причины остановки',
            },
        ),
        migrations.CreateModel(
            name='s_lift',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('ser_num', models.SmallIntegerField(verbose_name='Номер')),
                ('l_type', models.CharField(verbose_name='Тип', choices=[('Л', 'Лифт'), ('Э', 'Эскалатор')], max_length=1)),
                ('terminal', models.CharField(verbose_name='Терминал', choices=[('A', 'Терминал A'), ('B', 'Терминал B')], max_length=1)),
                ('location', models.CharField(verbose_name='Месторасположение, направление, этаж', max_length=50)),
            ],
            options={
                'verbose_name': 'Лифт/Эскалатор',
                'verbose_name_plural': 'Лифты/Эскалаторы',
                'ordering': ['ser_num'],
            },
        ),
        migrations.CreateModel(
            name='s_objects',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Название объекта', max_length=150)),
            ],
            options={
                'verbose_name': 'Объект',
                'verbose_name_plural': 'Объекты',
            },
        ),
        migrations.CreateModel(
            name='s_system',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('system_name', models.CharField(verbose_name='Название системы', max_length=50)),
                ('group', models.ForeignKey(verbose_name='Ответственная группа', to='otchet.s_group')),
            ],
            options={
                'verbose_name': 'Система',
                'verbose_name_plural': 'Системы',
                'ordering': ['system_name'],
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
            field=models.ForeignKey(verbose_name='Система', to='otchet.s_system'),
        ),
        migrations.AddField(
            model_name='s_fault',
            name='s_object',
            field=models.ForeignKey(verbose_name='Объект', to='otchet.s_objects'),
        ),
        migrations.AddField(
            model_name='s_drop_lift',
            name='fault',
            field=models.ForeignKey(verbose_name='Тип', to='otchet.s_fault_lift'),
        ),
        migrations.AddField(
            model_name='s_drop_lift',
            name='lift_name',
            field=models.ForeignKey(verbose_name='Название', to='otchet.s_lift'),
        ),
    ]
