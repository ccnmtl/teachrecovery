# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagetree', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodule',
            name='hierarchy',
            field=models.ForeignKey(default=1, to='pagetree.Hierarchy'),
            preserve_default=True,
        ),
    ]
