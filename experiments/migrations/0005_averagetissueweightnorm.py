# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0005_auto_20150409_0006'),
        ('experiments', '0004_relativeconcentration_experiment'),
    ]

    operations = [
        migrations.CreateModel(
            name='AverageTissueWeightNorm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('average', models.FloatField()),
                ('dataset', models.ForeignKey(to='experiments.Dataset')),
                ('protein', models.ForeignKey(to='atlas.Protein')),
                ('tissue', models.ForeignKey(null=True, to='atlas.Tissue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
