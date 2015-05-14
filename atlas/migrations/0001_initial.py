# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from='name', editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FunctionalGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from='name', editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.TextField()),
                ('gene_name', models.CharField(max_length=255)),
                ('protein_name', models.CharField(null=True, max_length=255)),
                ('species', models.CharField(null=True, max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from='gene_name', editable=False, blank=True)),
                ('family', models.ForeignKey(null=True, to='atlas.Family')),
                ('functional_group', models.ForeignKey(null=True, to='atlas.FunctionalGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tissue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from='name', editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='protein',
            name='tissues',
            field=models.ManyToManyField(null=True, related_name='proteins', to='atlas.Tissue'),
            preserve_default=True,
        ),
    ]
