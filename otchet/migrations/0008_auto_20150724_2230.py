# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0007_auto_20150724_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s_commit',
            name='s_prim',
            field=models.TextField(blank='True', null='True', verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='s_commit',
            name='s_staff_commit',
            field=models.ForeignKey(to='otchet.CustomUser', default=1),
            preserve_default=False,
        ),
    ]
