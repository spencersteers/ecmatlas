# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0003_externalsources'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProteinExternalReference',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('wikipedia_summary', models.TextField(null=True)),
                ('wikipedia_id', models.IntegerField(null=True)),
                ('wikipedia_url', models.URLField(null=True)),
                ('uniprot_id', models.IntegerField(null=True)),
                ('uniprot_url', models.URLField(null=True)),
                ('protein', models.OneToOneField(related_name='external_reference', to='atlas.Protein')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='externalsources',
            name='protein',
        ),
        migrations.DeleteModel(
            name='ExternalSources',
        ),
    ]
