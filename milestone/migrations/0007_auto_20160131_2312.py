# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0006_auto_20160131_2311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='millogin',
            options={'verbose_name_plural': 'Milestone Login', 'permissions': (('can_read_ml', 'Может читать'),), 'verbose_name': 'Milestone Login'},
        ),
    ]
