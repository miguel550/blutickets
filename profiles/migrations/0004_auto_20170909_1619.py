# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-09 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20170906_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number_primary',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number_primary_type',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number_secondary',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number_secondary_type',
            field=models.CharField(default='', max_length=15),
        ),
    ]
