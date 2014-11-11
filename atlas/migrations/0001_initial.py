# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecmdatabase', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TissueWeightNorm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('value', models.FloatField()),
                ('protein', models.ForeignKey(to='ecmdatabase.Protein', related_name='tissue_weight_norms')),
                ('tissue', models.ForeignKey(to='ecmdatabase.Tissue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
