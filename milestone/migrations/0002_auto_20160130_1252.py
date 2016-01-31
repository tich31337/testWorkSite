# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='millogin',
            name='lIP',
        ),
        migrations.AddField(
            model_name='millogin',
            name='lIP',
            field=models.ForeignKey(to='milestone.sysSec', default=1),
            preserve_default=False,
        ),
    ]
