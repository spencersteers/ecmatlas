# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0007_auto_20150503_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='averagerelativeconcentration',
            name='average',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='averagetissueweightnorm',
            name='average',
            field=models.FloatField(null=True),
        ),
    ]
