# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olymp', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ranking', models.FileField(upload_to='rankings')),
                ('olympiad', models.ForeignKey(to='olymp.Olympiad')),
            ],
        ),
    ]
