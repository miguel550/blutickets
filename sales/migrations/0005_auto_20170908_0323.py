# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 07:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20170906_1934'),
        ('sales', '0004_auto_20170907_0643'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_and_house', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=100)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Sector')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Address'),
        ),
    ]
