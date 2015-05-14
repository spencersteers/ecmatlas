# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0002_auto_20150406_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalSources',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('wikipedia_summary', models.TextField(null=True)),
                ('wikipedia_id', models.IntegerField(null=True)),
                ('wikipedia_url', models.URLField(null=True)),
                ('uniprot_id', models.IntegerField(null=True)),
                ('uniprot_url', models.URLField(null=True)),
                ('protein', models.OneToOneField(related_name='external_sources', to='atlas.Protein')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
