# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0004_auto_20150408_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proteinexternalreference',
            name='uniprot_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='proteinexternalreference',
            name='wikipedia_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
