# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0006_auto_20150724_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s_commit',
            name='s_staff_commit',
            field=models.ForeignKey(null='True', to='otchet.CustomUser', blank='True'),
        ),
    ]
