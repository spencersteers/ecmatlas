# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species', models.CharField(max_length=255)),
                ('peptide_sequence', models.TextField()),
                ('gene', models.CharField(max_length=255)),
                ('molecular_weight', models.FloatField()),
                ('peptide_note', models.CharField(max_length=255)),
                ('tissue_weight_norm', models.FloatField()),
                ('dataset', models.ForeignKey(to='experiments.Dataset', related_name='dataset_items')),
                ('family', models.ForeignKey(to='atlas.Family')),
                ('functional_group', models.ForeignKey(to='atlas.FunctionalGroup')),
                ('protein', models.ForeignKey(to='atlas.Protein', related_name='dataset_items')),
                ('tissue', models.ForeignKey(to='atlas.Tissue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(null=True, max_length=255)),
                ('aquisition_date', models.DateField(null=True)),
                ('species', models.CharField(null=True, max_length=255)),
                ('data_type', models.CharField(null=True, max_length=255)),
                ('aquisition_instrument', models.CharField(null=True, max_length=255)),
                ('aquisition_type', models.CharField(null=True, max_length=255)),
                ('publication', models.URLField(null=True)),
                ('data_depository_link', models.CharField(null=True, max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from='get_full_name', editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelativeConcentration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(null=True, max_length=255)),
                ('disease_state', models.CharField(null=True, max_length=255)),
                ('disease_note', models.CharField(null=True, max_length=255)),
                ('age', models.IntegerField(null=True)),
                ('value', models.FloatField()),
                ('dataset', models.ForeignKey(to='experiments.Dataset')),
                ('protein', models.ForeignKey(to='atlas.Protein')),
                ('tissue', models.ForeignKey(to='atlas.Tissue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dataset',
            name='experiment',
            field=models.ForeignKey(null=True, to='experiments.Experiment'),
            preserve_default=True,
        ),
    ]
