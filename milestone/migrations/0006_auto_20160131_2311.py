# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0005_syssec_miadmin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='millogin',
            options={'verbose_name': 'Milestone Login', 'permissions': 'can_read_ml', 'verbose_name_plural': 'Milestone Login'},
        ),
    ]
