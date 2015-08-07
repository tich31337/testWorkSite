# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otchet', '0002_auto_20150718_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='birthday',
        ),
    ]
