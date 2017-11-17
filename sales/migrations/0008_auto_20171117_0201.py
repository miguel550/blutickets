# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-17 06:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_lineitem_ttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineitem',
            name='ttype',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.Type'),
        ),
    ]
