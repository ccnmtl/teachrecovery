# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_usermodule_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodule',
            name='hierarchy',
            field=models.ForeignKey(default=1, verbose_name=b'Course', to='pagetree.Hierarchy'),
            preserve_default=True,
        ),
    ]
