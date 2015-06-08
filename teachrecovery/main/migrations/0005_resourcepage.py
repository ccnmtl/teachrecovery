# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
        ('pagetree', '0001_initial'),
        ('main', '0004_auto_20150430_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourcePage',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='flatpages.FlatPage')),
                ('hierarchy', models.ForeignKey(default=1, verbose_name=b'Course', to='pagetree.Hierarchy')),
            ],
            options={
            },
            bases=('flatpages.flatpage',),
        ),
    ]
