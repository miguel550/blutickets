# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_auto_20170908_0557'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.Ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='tickettype',
            name='ttype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.Type'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_types',
            field=models.ManyToManyField(through='tickets.TicketType', to='tickets.Type'),
        ),
    ]