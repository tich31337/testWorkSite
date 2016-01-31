# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0004_auto_20160131_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='syssec',
            name='miAdmin',
            field=models.BooleanField(verbose_name='Администратор Milestone', default=False),
        ),
    ]
