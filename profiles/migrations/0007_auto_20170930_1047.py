# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20170926_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Municipality'),
        ),
    ]
