# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olymp', '0003_auto_20170415_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='olympiad',
            name='president',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='olymp.Person'),
        ),
    ]