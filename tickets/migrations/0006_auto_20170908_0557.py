# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 09:57
from __future__ import unicode_literals

from django.db import migrations, models
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_remove_ticket_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='_description_rendered',
            field=models.TextField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='description_markup_type',
            field=models.CharField(choices=[('', '--'), ('html', 'HTML'), ('plain', 'Plain'), ('markdown', 'Markdown'), ('restructuredtext', 'Restructured Text')], default='markdown', max_length=30),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=markupfield.fields.MarkupField(rendered_field=True),
        ),
    ]
