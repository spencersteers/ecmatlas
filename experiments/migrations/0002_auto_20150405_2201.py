# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='aquisition_instrument',
            new_name='acquisition_instrument',
        ),
        migrations.RenameField(
            model_name='experiment',
            old_name='aquisition_type',
            new_name='acquisition_type',
        ),
    ]
