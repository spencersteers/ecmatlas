# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0005_auto_20150409_0006'),
        ('experiments', '0006_auto_20150503_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='averagerelativeconcentration',
            name='tissue',
            field=models.ForeignKey(to='atlas.Tissue', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='relativeconcentration',
            name='protein',
            field=models.ForeignKey(to='atlas.Protein', related_name='relative_concentrations'),
        ),
    ]
