# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0005_auto_20150409_0006'),
        ('experiments', '0005_averagetissueweightnorm'),
    ]

    operations = [
        migrations.CreateModel(
            name='AverageRelativeConcentration',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('tissue_state', models.CharField(max_length=255, null=True)),
                ('average', models.FloatField()),
                ('protein', models.ForeignKey(related_name='average_relative_concentrations', to='atlas.Protein')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='averagetissueweightnorm',
            name='dataset',
        ),
        migrations.AlterField(
            model_name='averagetissueweightnorm',
            name='protein',
            field=models.ForeignKey(related_name='average_tissue_weight_norms', to='atlas.Protein'),
        ),
    ]
