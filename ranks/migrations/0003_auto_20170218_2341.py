# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranks', '0002_ranking_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='processed',
            field=models.TimeField(null=True, default=None),
        ),
    ]
