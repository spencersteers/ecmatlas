# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protein',
            name='gene_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
