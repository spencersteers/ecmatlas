# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0003_auto_20150406_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='relativeconcentration',
            name='experiment',
            field=models.ForeignKey(related_name='relative_concentrations', default=1, to='experiments.Experiment'),
            preserve_default=False,
        ),
    ]
