# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('party_name', models.CharField(max_length=150)),
                ('flyer_image', models.ImageField(upload_to='')),
                ('direction', models.CharField(max_length=250)),
                ('description', models.TextField()),
            ],
        ),
    ]
