# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(null=True, max_length=255)),
                ('data_file', models.FileField(upload_to='uploads/datasets')),
                ('is_inserted', models.BooleanField(default=False)),
                ('inserted_at', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatasetItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('species', models.CharField(max_length=255)),
                ('peptide_sequence', models.TextField()),
                ('gene', models.CharField(max_length=255)),
                ('molecular_weight', models.FloatField()),
                ('peptide_note', models.CharField(max_length=255)),
                ('tissue_weight_norm', models.FloatField()),
                ('dataset', models.ForeignKey(related_name='dataset_items', to='experiments.Dataset')),
                ('family', models.ForeignKey(to='atlas.Family')),
                ('functional_group', models.ForeignKey(to='atlas.FunctionalGroup')),
                ('protein', models.ForeignKey(related_name='dataset_items', to='atlas.Protein')),
                ('tissue', models.ForeignKey(to='atlas.Tissue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
