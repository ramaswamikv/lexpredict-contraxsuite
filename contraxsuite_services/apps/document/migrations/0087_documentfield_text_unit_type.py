# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-06 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0086_textunit_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfield',
            name='text_unit_type',
            field=models.CharField(choices=[('sentence', 'sentence'), ('paragraph', 'paragraph'), ('section', 'section')], db_index=True, default='sentence', max_length=10),
        ),
    ]
