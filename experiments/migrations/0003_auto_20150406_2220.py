# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0002_auto_20150405_2201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='aquisition_date',
            new_name='acquisition_date',
        ),
        migrations.AlterField(
            model_name='dataset',
            name='experiment',
            field=models.ForeignKey(to='experiments.Experiment', null=True, related_name='datasets'),
        ),
    ]
