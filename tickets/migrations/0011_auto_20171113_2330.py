# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-14 03:30
from __future__ import unicode_literals

from django.db import migrations, models
import tickets.models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_ticket_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='slug',
            field=models.SlugField(default=tickets.models.random_string, unique=True),
        ),
    ]
