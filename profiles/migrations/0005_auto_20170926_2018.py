# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 00:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20170909_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Province')),
            ],
        ),
        migrations.AlterField(
            model_name='sector',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Province'),
        ),
        migrations.AddField(
            model_name='sector',
            name='municipality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Municipality'),
        ),
    ]
